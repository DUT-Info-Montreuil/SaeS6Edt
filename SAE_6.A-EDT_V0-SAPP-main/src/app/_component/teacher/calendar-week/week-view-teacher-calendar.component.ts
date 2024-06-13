import { Component, OnInit, HostListener, Input } from '@angular/core';
import { CalendarEvent, CalendarView } from 'angular-calendar';
import { adapterFactory } from 'angular-calendar/date-adapters/moment';
import * as moment from 'moment';
import { Subject, forkJoin } from 'rxjs';
import { DatePipe } from '@angular/common';
import { TeacherService } from '../../../_service/teacher.service';
import { Teacher } from '../../../_model/entity/teacher.model';
import { CourseService } from '../../../_service/course.service';
import { Course } from '../../../_model/entity/course.model';
import { ResourceService } from '../../../_service/resource.service';
import { Resource } from '../../../_model/entity/resource.model';
import { Group } from '../../../_model/entity/group.model';
import { GroupService } from '../../../_service/group.service';
import { format } from 'date-fns';
import { ToastrService } from 'ngx-toastr';
import { RoomService } from 'src/app/_service/room.service';
import { Promotion } from 'src/app/_model/entity/promotion.model';
import { PromotionService } from 'src/app/_service/promotion.service';
import { ViewEncapsulation } from '@angular/core';
import { User } from 'src/app/_model/entity/user.model';
import { ChangePasswdComponent } from '../../general/change-passwd/change-passwd.component';
import { MatDialog } from '@angular/material/dialog';

export function momentAdapterFactory() {
  return adapterFactory(moment);
};

@Component({
  selector: 'app-calendar-week-view-teacher',
  templateUrl: './week-view-teacher-calendar.component.html',
  styleUrls: ['./week-view-teacher-calendar.component.scss'],
  encapsulation: ViewEncapsulation.None,
})

export class WeekViewTeacherCalendarComponent implements OnInit {

  @Input() user: User;

  courses: Course[] = [];
  teachers: Teacher[] = [];
  salles: any[] = [];
  ressources: Resource[] = [];
  groupes: Group[] = [];
  promos: Promotion[] = [];

  courseForEdit: Course;

  isWeekCalendar = true;
  viewPhone = false;

  args: any[] = [];

  public eventSelectionne: any = null;

  idUser: any;

  showModalMod = false;
  showModalAdd = false;
  showModalStats = false;

  viewDate: Date = new Date();
  view: CalendarView = CalendarView.Week;

  events: CalendarEvent[] = [];
  eventsToPushToBd: CalendarEvent[] = [];

  isDrawerOpen = false;

  refresh = new Subject<void>();

  /*
    @function getIndex
    @param event: any
    @desc Returns the index of the specified event in the events array
  */
  getIndex(event: any){
      return this.events.indexOf(event.event);
  }
  
  constructor(
    private datePipe: DatePipe,
    private teacherService: TeacherService,
    private courseService: CourseService,
    private resourceService: ResourceService,
    private groupService: GroupService,
    private toastr: ToastrService,
    private roomService: RoomService,
    private promotionService: PromotionService,
    private dialog: MatDialog
  ) {}
  
  /*
    @function toggleDrawer
    @desc Toggles the state of the drawer (open/close)
  */
  toggleDrawer() {
    this.isDrawerOpen = !this.isDrawerOpen;
  }

  /*
      @function openModalPasswd
      @desc: open modal change password
  */
  openModalPasswd(){
    this.dialog.open(ChangePasswdComponent);
  }
  
  /*
    @function onResize
    @param event: Event
    @desc Handles the window resize event and updates the view
  */
  @HostListener('window:resize', ['$event'])
  onResize(event: Event): void {
    this.updateView();
  }
  
  /*
    @function updateView
    @desc Updates the view based on the window width
  */
  private updateView(): void {
    const largeurEcran = window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth;
    this.isWeekCalendar = largeurEcran > 690;
    this.viewPhone = largeurEcran > 690;
  }
  
  ngOnInit(): void {
    this.idUser = this.user.id;
    this.updateView();
    forkJoin([
      this.teacherService.getTeachers(), 
      this.roomService.getSalles(), 
      this.resourceService.getResources(), 
      this.groupService.getGroups(),
      this.promotionService.getPromotions()
  
    ]).subscribe({
      next: data  => {
        this.teachers = data[0]
        this.salles = data[1]
        this.ressources = data[2]
        this.groupes = data[3]
        this.promos = data[4]
        this.loadEvents();
      },
      error :error => {
        console.log(error);
      }
    });
  }
  
  /*
    @function toggleWeekCalendar
    @desc Toggles the view between week and day calendar
  */
  toggleWeekCalendar(){
    this.isWeekCalendar = !this.isWeekCalendar;
  }
  
  /*
    @function changeViewDay
    @param event: any
    @desc Updates the viewDate based on the selected day
  */
  changeViewDay(event : any){
    this.viewDate = new Date(event.day.date);
    this.toggleWeekCalendar();
  }
  
  /*
    @function openModalMod
    @param eventId: number
    @desc Opens the modal for modifying the specified event
  */
  openModalMod(eventId: number) {
    this.courseForEdit = this.getCourseByEventId(eventId)!;
    this.showModalMod = true;
  }
  
  /*
    @function closeModalMod
    @desc Closes the modify modal and updates the event start and end times
  */
  closeModalMod() {
    this.showModalMod = false;
    this.eventSelectionne.event.start = Date.parse(this.eventSelectionne.event.start);
    this.eventSelectionne.event.end = Date.parse(this.eventSelectionne.event.end);
  }
  
  /*
    @function openModalAdd
    @desc Opens the modal for adding a new event
  */
  openModalAdd() {
    this.showModalAdd = true;
  }
  
  /*
    @function closeModalAdd
    @desc Closes the add modal for new event
  */
  closeModalAdd() {
    this.showModalAdd = false;
  }
  
  /*
    @function addArguments
    @param args: any
    @desc Adds the specified arguments to the existing arguments, removing any existing argument with the same key
  */
  addArguments(args: any){
    // Remove existing arguments with the same key
    this.args = this.args.filter(arg => Object.keys(arg)[0] != Object.keys(args)[0]);
    // Add the new arguments
    this.args.push(args);
  }

  /*
    @function loadEvents
    @desc Loads events from the server and updates the view
  */
  loadEvents(){
    if (this.args.length > 2 && this.args.find(arg => Object.keys(arg)[0] == "method") == undefined){
      this.args.push({method: "filter"});
    }

    this.events = [];

    let day = this.viewDate.getDay();
    let diff = this.viewDate.getDate() - day + (day == 0 ? -6:1);
    let date_temp = new Date(this.viewDate);
    let monday = new Date(date_temp.setDate(diff));
    let friday = new Date(date_temp.setDate(diff + 4));

    this.addArguments({date_min: format(monday, 'yyyy-MM-dd')});
    this.addArguments({date_max: format(friday, 'yyyy-MM-dd')});

    this.courseService.getCourses(this.args).subscribe({
      next : courses => {
        this.courses = courses;
        this.events = [];
        for (let course of courses) {
          this.addEvent(course);
        }
        this.refresh.next();

      },
      error: error => {
        console.log(error);
      }
    });
  }

  /*
    @function addCourse
    @desc Adds a new course to the list and triggers the addition of an event
  */
  addCourse(course: Course) {
    this.courses.push(course);
    this.addEvent(course);
  }

  /*
    @function addEvent
    @desc Adds an event for the given course
  */
  addEvent(course: Course): void {
    let cssClass : string;
    if (this.args.find(arg => Object.keys(arg)[0] == "group") != undefined){
      cssClass = `calendar-user-position-${this.getPosition(course)} calendar-user-width-${this.getWidth(course)}`;
    }
    else {
      cssClass = ``;
    }

    this.events.push({
      id: course.id,
      title: course.initial_ressource,
      start: new Date(course.start_time),
      end: new Date(course.end_time),
      color: {
        primary: "#FFFFFF",
        secondary: this.getResourceByInitial(course.initial_ressource)!.color,
      },        
      draggable: false,
      resizable: {
        beforeStart: false,
        afterEnd: false,
      },
      cssClass: cssClass
    });
  }

  /*
    @function getWidth
    @desc Calculates the width of the course based on its group hierarchy
  */
  getWidth(course: Course): number {
    let group = this.groupes.find(group => group.id == course.id_group);
    let width = 100
    while (group && group.id_group_parent != null){
      const groupsInParent = this.groupes.filter(group_curr => group_curr.id_group_parent == group!.id_group_parent);
      width = width / groupsInParent.length;
      group = this.groupes.find(group_curr => group_curr.id == group!.id_group_parent);
    }
    return Math.ceil(width)
  }

  /*
    @function getPosition
    @desc Calculates the position of the course based on its group hierarchy
  */
  getPosition(course: Course): number {
    let group = this.groupes.find(group => group.id == course.id_group);
    let pourcents: any[] = []
    while (group && group.id_group_parent != null){
      const groupsInParent = this.groupes.filter(group_curr => group_curr.id_group_parent == group!.id_group_parent);
      const index = groupsInParent.indexOf(group!);
      pourcents.push({index: index, length: groupsInParent.length})
      group = this.groupes.find(group_curr => group_curr.id == group!.id_group_parent);
    }
    let left = 0
    if (pourcents.length > 0){
      const last = pourcents.pop()
      let parentPourcent = 100 / last.length
      left = last.index * parentPourcent
      
      for (let item of pourcents.reverse()){
        parentPourcent = parentPourcent / item.length
        left = left + item.index * parentPourcent
      }
    }
    return Math.ceil(left);
  }

  /*
    @function removeCourse
    @desc Removes the specified course from the list of courses and events
  */
  removeCourse(course_remove: Course): void {
    this.courses = this.courses.filter((course) => course.id !== course_remove.id);
    this.events = this.events.filter((event) => event.id !== course_remove.id);
  }

  /*
    @function eventClicked
    @desc Handles the click event on a calendar event
  */
  eventClicked(event: any) {
    this.eventSelectionne = event;
  
    Promise.all([this.loadEventStart(this.eventSelectionne), this.loadEventEnd(this.eventSelectionne)])
      .then(([loadedEventStart, loadedEventEnd]) => {
        this.updateDateStart(loadedEventStart);
        this.updateDateEnd(loadedEventEnd);
        this.openModalMod(this.eventSelectionne.event.id);
      }
    );
  }
  
  /*
    @function loadEventStart
    @desc Loads the start time of the specified event
  */
  loadEventStart(event: any): Promise<Date> {
    return new Promise<Date>((resolve, reject) => {
      setTimeout(() => {
        const loadedEventStart = event.event.start;
        resolve(loadedEventStart);
      }, 100);
    });
  }
  
  /*
    @function loadEventEnd
    @desc Loads the end time of the specified event
  */
  loadEventEnd(event: any): Promise<Date> {
    return new Promise<Date>((resolve, reject) => {
      setTimeout(() => {
        const loadedEventEnd = event.event.end;
        resolve(loadedEventEnd);
      }, 100);
    });
  }

  /*
    @function onSubmitMod
    @desc Handles the submission of a form for modifying an event
  */
  onSubmitMod(){
    this.closeModalMod();
  }

  /*
    @function eventTimesChanged
    @desc Handles the change of the start and end times of an event
  */
  eventTimesChanged(event: any) {
    let course_find = this.courses.find(course => course.id == event.event.id);
    if (!course_find){
      return;
    }
    
    course_find.start_time = event.newStart;
    course_find.end_time = event.newEnd;

    const event_backup = this.events.find(event => event.id == course_find!.id);

    this.events = this.events.filter((event) => event.id !== course_find!.id);
    this.addEvent(course_find);

    this.courseService.updateCourse(course_find).subscribe({
      next: course => {
        this.courses.filter((course) => course.id !== course_find!.id);
        this.events = this.events.filter((event) => event.id !== course_find!.id);
        this.addCourse(course);
      },
      error: response => {
        console.log(response);
        this.events = this.events.filter((event) => event.id !== course_find!.id);
        this.events.push(event_backup!);
        this.toastr.error(response.error.error, 'Erreur',{timeOut: 2000});
      }
    });
  }

  /*
    @function eventTimesChanged
    @desc Handles the change of the start and end times of an event
  */
  endTimeChanged(newEvent: any, ancienneDate: string) {
    newEvent.event.end = Date.parse(ancienneDate);
    this.refresh.next();
    this.updateDateEnd(newEvent.event.end);
  }

  /*
    @function startTimeChanged
    @desc Handles the change of the start time of an event
  */
  startTimeChanged(newEvent: any, ancienneDate: string) {
    newEvent.event.start = Date.parse(ancienneDate);
    this.refresh.next();
    this.updateDateStart(newEvent.event.start);
  }

  /*
    @function updateDateStart
    @desc Updates the start date of an event
  */
  updateDateStart(date: Date) {
    this.eventSelectionne.event.start = this.datePipe.transform(date, 'yyyy-MM-ddTHH:mm');
  }

  /*
    @function updateDateEnd
    @desc Updates the end date of an event
  */
  updateDateEnd(date: Date) {
    this.eventSelectionne.event.end = this.datePipe.transform(date, 'yyyy-MM-ddTHH:mm');
  }

  /*
    @function supprimerCours
    @desc Removes an event from the list of events
  */
  supprimerCours(event: any){
    this.events.splice(this.getIndex(event), 1);
    this.refresh.next();
    this.closeModalMod();
  }

  /*
    @function getCourseByEventId
    @desc Returns the course associated with an event
  */
  getCourseByEventId(eventId: number) {
    return this.courses.find(course => course.id == eventId);
  }

  onDateChange(event: Event): void {
    const inputElement = event.target as HTMLInputElement;
    const selectedDate = inputElement.value;
    this.viewDate = new Date(selectedDate);
  }
  
  /*
    @function getRessourceNameByInitial
    @desc Returns the name of the resource based on its initial
  */
  getRessourceNameByInitial(initial_resource: string) {
      return this.ressources.find(resource => resource.initial == initial_resource)?.name;
  }
  
  /*
    @function getResourceByInitial
    @desc Returns the resource object based on its initial
  */
  getResourceByInitial(initial_resource: string) {
      return this.ressources.find(resource => resource.initial == initial_resource);
  }
  
  /*
    @function getTimeString
    @desc Returns the time string formatted as 'HH:mm' based on the input date
  */
  getTimeString(date: Date) {
      return this.datePipe.transform(date, 'HH:mm');
  }
  
  /*
    @function getInitialTeacher
    @desc Returns the initial of the teacher associated with the specified course ID
  */
  getInitialTeacher(id: number) {
      let id_teacher =  this.courses.find(course => course.id == id)?.id_enseignant;
      let teacher = this.teachers.find(teacher => teacher.id == id_teacher);
      return teacher? teacher.staff.initial : "";
  }
  
  /*
    @function publishCourse
    @desc Publishes the courses and handles success and error notifications
  */
  publishCourse(){
      this.courseService.publishCourses().subscribe({
        next:() => {
          this.toastr.success('Les cours ont été publiés', 'Succès',{timeOut: 1500,});
          this.loadEvents()
        },
        error: error => {
          this.toastr.error(error, 'Erreur',{timeOut: 2000});
        }
      });
  }
  
  /*
    @function cancelCourse
    @desc Cancels the courses and handles success and error notifications
  */
  cancelCourse(){
      this.courseService.cancelCourses().subscribe({
        next:() => {
          this.toastr.success('Les cours ont été annulés', 'Succès',{timeOut: 1500});
          this.loadEvents()
        },
        error: error => {
          this.toastr.error(error, 'Erreur',{timeOut: 2000});
        }
      });
  }
  
  /*
    @function filterByPromo
    @desc Filters the events by promotion group and loads the filtered events
  */
  filterByPromo(event: any){
      const promo = this.promos.find(promo => promo.id == event.target.value)!
      const arg = {group: promo.group.id};
      this.addArguments(arg);
      this.loadEvents();
  }
  
  /*
    @function filterByRoom
    @desc Filters the events by room and loads the filtered events
  */
  filterByRoom(event: any){
      const arg = {room: event.target.value};
      this.addArguments(arg);
      this.loadEvents();
  }
  
  /*
    @function filterByTeacher
    @desc Filters the events by teacher and loads the filtered events
  */
  filterByTeacher(event: any){
      const arg = {teacher: event.target.value};
      this.addArguments(arg);
      this.loadEvents();
  }
  
  /*
    @function removeFilter
    @desc Removes the specified filter and loads the events
  */
  removeFilter(key: string, select: any){
      this.args = this.args.filter(arg => Object.keys(arg)[0] != key);
      if (this.args.length <= 3){
        this.args = this.args.filter(arg => Object.keys(arg)[0] != 'method');
      }
      this.loadEvents();
      select.value = "";
  }
  
  /*
    @function openModalStats
    @desc Opens the statistics modal
  */
  openModalStats() {
      this.showModalStats = true;
  }
  
  /*
    @function closeModalStats
    @desc Closes the statistics modal
  */
  closeModalStats() {
      this.showModalStats = false;
  }
  
  /*
    @function disablePreventDefault
    @desc Disables the default behavior of the specified event
  */
  disablePreventDefault(event: any){
      event.preventDefault();
  }
  
  /*
    @function redirectToLogout
    @desc Redirects to the logout page after disabling the default behavior of the specified event
  */
  redirectToLogout(event: any){
      this.disablePreventDefault(event);
      window.location.href = "/logout";
  }
}