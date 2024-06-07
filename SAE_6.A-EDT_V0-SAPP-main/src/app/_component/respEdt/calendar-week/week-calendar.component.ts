import { HostListener, Component, OnInit, Input } from '@angular/core';
import { CalendarEvent, CalendarView, DAYS_OF_WEEK } from 'angular-calendar';
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
import { addDays, format, getWeek, startOfWeek } from 'date-fns';
import { ToastrService } from 'ngx-toastr';
import { RoomService } from 'src/app/_service/room.service';
import { WeekCommentService } from 'src/app/_service/weekComment.service';
import { WeekComment } from 'src/app/_model/entity/weekComment.model';
import { Promotion } from 'src/app/_model/entity/promotion.model';
import { EdtManagerService } from 'src/app/_service/edtManager.service';
import { ViewEncapsulation} from '@angular/core';
import { UserService } from 'src/app/_service/user.service';
import { User } from 'src/app/_model/entity/user.model';
import { MatDialog } from '@angular/material/dialog';
import { ChangePasswdComponent } from '../../general/change-passwd/change-passwd.component';
import { AffiliationRessourcePromo } from 'src/app/_service/affiliationRessourcePromo.service';

export function momentAdapterFactory() {
  return adapterFactory(moment);
};

@Component({
  selector: 'app-calendar-week-view-resp-edt',
  templateUrl: './week-calendar.component.html',
  styleUrls: ['./week-calendar.component.scss'],
  encapsulation: ViewEncapsulation.None,
})

export class WeekCalendarComponent implements OnInit {

  @Input() user: User;
  courses: Course[] = [];
  teachers: Teacher[] = [];
  salles: any[] = [];
  ressources: Resource[] = [];
  groupes: Group[] = [];
  comments: WeekComment[] = [];

  ressourcesShow: Resource[] = [];
  group_show: Group[] = [];
  excludedDaysList: number[] = [0, 6];

  promoManaged: Promotion[] = [];
  promoSelected: Promotion = new Promotion();

  brouillon: boolean = false;
  isDraftActive: boolean = false;

  loading = true;

  showModalComment = false;
  showModalFlopEdt = false;

  courseForEdit: Course | null;
  coursesToPaste: Course[] = [];

  isWeekCalendar = true;
  viewPhone = false;

  selectedDays: {name: string, selected: boolean, date: Date}[] = [];

  idUser: any;

  pasteEnable: boolean = false;

  public eventSelectionne: any = null;

  isDrawerOpen = false;

  showModalPasswd = false;
  showModalMod = false;
  showModalAdd = false;
  showModalCopy = false;
  showModalPaste = false;
  showModalStats = false;
  showModalChoice = false;

  viewDate: Date = new Date();
  view: CalendarView = CalendarView.Week;

  events: CalendarEvent[] = [];
  eventsToPushToBd: CalendarEvent[] = [];

  refresh = new Subject<void>();

  /*
      @function getIndex
      @param event: any
      @return number
      @desc: get index of event
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
    private weekCommentService: WeekCommentService,
    private edtManagerService: EdtManagerService,
    private userService: UserService,
    private dialog: MatDialog,
    private affRessourcePromoService: AffiliationRessourcePromo
    ) {
  }

  print(obj: any){
    console.log(obj);
  }

  changeBrouillonValue(){
    if (!this.brouillon){
      this.brouillon = true;
    }
  }

  /*
      @function toggleDrawer
      @desc: toggle drawer
  */
  toggleDrawer() {
    this.isDrawerOpen = !this.isDrawerOpen;
  }

  /*
      @function onResize
      @param event: Event
      @desc: on resize
  */
  @HostListener('window:resize', ['$event'])
  onResize(event: Event): void {
    this.updateView();
  }

  /*
      @function updateView
      @desc: update view
  */
  private updateView(): void {
    const largeurEcran = window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth;
    this.isWeekCalendar = largeurEcran > 768;
    this.viewPhone = largeurEcran > 1466;
  }

  activateDraft(){
    this.isDraftActive = !this.isDraftActive;
    if (this.excludedDaysList.length == 2){
      this.excludedDaysList = [0];
    } else {
      this.excludedDaysList = [0, 6];
    }
  }

  /*
      @function ngOnInit
      @desc: on init
  */
  ngOnInit(): void {
    this.updateView();
    forkJoin([
      this.teacherService.getTeachers(),
      this.roomService.getSalles(),
      // this.resourceService.getResources(),
      this.groupService.getGroups(),
      this.weekCommentService.getComments(),
      this.edtManagerService.getPromoEdtManager(),
    ]).subscribe({
      next: data  => {
        this.teachers = data[0].filter(teacher => teacher.activated);
        this.salles = data[1]
        this.groupes = data[2]
        this.comments = data[3]
        this.promoManaged = data[4]
        if (this.promoManaged.length > 0){
          this.promoSelected = this.promoManaged[0];
          this.refreshRessources();
        }
        this.loadEvents();
        this.loading = false;
        console.log(this.events);
      },
      error :error => {
        this.toastr.error("un problème est survenue lors du chargement" + error.message);
      }
    });
    this.userService.getIdentify().subscribe({
      next: user => {
        this.idUser = user.id;
      },
      error: error => {
      }
    })
  }

  refreshRessources(){
    this.affRessourcePromoService.getRessourceByPromo(this.promoSelected.id).subscribe({
      next: response => {
        this.ressources = response;
      },
      error: error => {
        console.log(error);
      }
    });
  }

  /*
      @function setViewDate
      @desc: set view date
  */
  setViewDate(){
    let day = this.viewDate.getDay();
    let diff = this.viewDate.getDate() - day + (day == 0 ? -6:1);

    if (this.viewDate.getDay() == 0){this.viewDate.setDate(this.viewDate.setDate(1));}
  }

  getWeek(date: Date) {
    const dayOfWeek = date.getDay(); // Obtient le jour de la semaine (0 = dimanche, 1 = lundi, ..., 6 = samedi)
    const diff = date.getDate() - dayOfWeek; // Calcul de la différence pour obtenir le dimanche de la semaine
    const sunday = new Date(date); // Crée une nouvelle instance de Date basée sur la date d'origine
    sunday.setDate(diff);
    return getWeek(sunday, { weekStartsOn: 0 });
  }

  changePromotion(event: any){
    let id_promo = event.target.value;
    this.promoSelected = this.promoManaged.find(promo => promo.id == id_promo)!;
    this.refreshRessources();
    this.loadEvents();
  }

  /*
      @function addOrUpdateComment
      @param comment: WeekComment
      @desc: add or update comment
  */
  addOrUpdateComment(comment: WeekComment){
    let index = this.comments.findIndex(comment_find => comment_find.id == comment.id);
    if (index == -1){
      this.comments.push(comment);
    }else{
      this.comments[index] = comment;
    }
  }

  /*
      @function deleteComment
      @param comment: WeekComment
      @desc: delete comment
  */
  deleteComment(comment: WeekComment){
    this.comments = this.comments.filter(comment_find => comment_find.id != comment.id);
  }

  /*
      @function openModalPasswd
      @desc: open modal change password
  */
  openModalPasswd(){
    this.dialog.open(ChangePasswdComponent);
  }


  /*
      @function openModalAdd
      @desc: open modal add
  */
  openModalAdd() {
    this.showModalAdd = true;
  }

  /*
      @function closeModalAdd
      @desc: close modal add
  */
  closeModalAdd() {
    this.showModalAdd = false;
  }

  /*
      @function openModalStats
      @desc: open modal stats
  */
  openModalStats() {
    this.showModalStats = true;
  }

  /*
      @function closeModalStats
      @desc: close modal stats
  */
  closeModalStats() {
    this.showModalStats = false;
  }


  /*
      @function getComment
      @param date: Date
      @return WeekComment
  */
  getComment(date : Date){
    let week_number = this.getWeek(date);
    let year = date.getFullYear().toString();
    return this.comments.find(comment => comment.week_number == week_number && comment.year == year && comment.id_promo == this.promoSelected.id);
  }

  /*
      @function toggleModalComment
      @desc: toggle modal comment
  */
  toggleModalComment(){
    this.showModalComment = !this.showModalComment;
  }

  /*
      @function openModalCopy
      @desc: open modal copy
  */
  openModalCopy() {
    this.showModalCopy = true;
  }

  /*
      @function closeModalCopy
      @desc: close modal copy
  */
  closeModalCopy() {
    this.showModalCopy = false;
    this.brouillon = true;
  }

  /*
      @function toogleModalFlopEdt
      @desc: open modal flop edt
   */
  toggleModalFlopEdt(){
    this.showModalFlopEdt = !this.showModalFlopEdt;
  }



  /*
      @function openModalPaste
      @desc: open modal paste
  */
  openModalPaste() {
    this.showModalPaste = true;
  }

  /*
      @function closeModalPaste
      @desc: close modal paste
  */
  closeModalPaste() {
    this.showModalPaste = false;
    this.refresh.next();
  }

  /*
      @function loadEvents
      @desc: load events
  */
  loadEvents(){
    this.showModalComment = false;
    this.events = [];

    let day = this.viewDate.getDay();
    let diff = this.viewDate.getDate() - day + 1;
    let date_temp = new Date(this.viewDate);
    let monday = new Date(date_temp.setDate(diff));
    let saturday = new Date(date_temp.setDate(diff + 5));

    const args = [{date_min: format(monday, 'yyyy-MM-dd')}, {date_max: format(saturday, 'yyyy-MM-dd')}, {group: this.promoSelected.group.id}];

    this.courseService.getCourses(args).subscribe({
      next : courses => {
        this.courses = courses;
        this.events = [];
        for (let course of courses) {
          this.addEvent(course);
        }
        this.refresh.next();
        this.ressourcesShow = this.ressources;
        this.getGroupTree();
      },
      error: error => {
      }
    });
  }

  /*
      @function redirectToUtilitaires
      @desc: redirect to page utilitaires
  */
  redirectToUtilitaires(){
    window.location.href = "/ajout";
  }

  /*
      @function redirectToGestionGroupes
      @desc: redirect to page gestion groupes
  */
  redirectToGestionGroupes(){
    window.location.href = "/groupes";
  }

  /*
      @function addCourse
      @param course: Course
      @desc: add course
  */
  addCourse(course: Course) {
    this.courses.push(course);
    this.addEvent(course);
    this.refresh.next();
  }

  /*
      @function addEvent
      @param course: Course
      @desc: add event
  */
  addEvent(course: Course): void {
    this.events.push({
      id: course.id,
      title: course.initial_ressource,
      start: new Date(course.start_time),
      end: new Date(course.end_time),
      color: {
        primary: "#FFFFFF",
        secondary: this.getRessourcesByInitial(course.initial_ressource)!.color,
      },
      draggable: true,
      resizable: {
        beforeStart: true,
        afterEnd: true,
      },
      cssClass: `calendar-position-${this.getPosition(course)} calendar-width-${this.getWidth(course)}`
    });
  }

  /*
      @function getWidth
      @param course: Course
      @return number
      @desc: get width
  */
  getWidth(course: Course): number {
    let group = this.groupes.find(group => group.id == course.id_group);
    let width = 100;
    while (group && group.id_group_parent != null){
      const groupsInParent = this.groupes.filter(group_curr => group_curr.id_group_parent == group!.id_group_parent);
      width = width / groupsInParent.length;
      group = this.groupes.find(group_curr => group_curr.id == group!.id_group_parent);
    }
    return Math.ceil(width)
  }

  /*
      @function getPosition
      @param course: Course
      @return number
      @desc: get position
  */
  getPosition(course: Course): number {
    let group = this.groupes.find(group => group.id == course.id_group);
    let pourcents: any[] = [];
    while (group && group.id_group_parent != null){
      const groupsInParent = this.groupes.filter(group_curr => group_curr.id_group_parent == group!.id_group_parent);
      const index = groupsInParent.indexOf(group!);
      pourcents.push({index: index, length: groupsInParent.length});
      group = this.groupes.find(group_curr => group_curr.id == group!.id_group_parent);
    }
    let left = 0;
    if (pourcents.length > 0){
      const last = pourcents.pop();
      let parentPourcent = 100 / last.length;
      left = last.index * parentPourcent;

      for (let item of pourcents.reverse()){
        parentPourcent = parentPourcent / item.length;
        left = left + item.index * parentPourcent;
      }
    }
    return Math.ceil(left);
  }

  removeCourse(course_remove: Course): void {
    this.courses = this.courses.filter((course) => course.id !== course_remove.id);
    this.events = this.events.filter((event) => event.id !== course_remove.id);
  }

  /*
      @function toggleWeekCalendar
      @desc: toggle week calendar
  */
  toggleWeekCalendar(){
    this.isWeekCalendar = !this.isWeekCalendar;
  }

  /*
      @function changeViewDay
      @param event: any
      @desc: change view day
  */
  changeViewDay(event : any){
    this.viewDate = new Date(event.day.date);
    this.toggleWeekCalendar()
  }


  /*
      @function getGroupTree
      @desc: get group tree and set group show
  */
  getGroupTree(){
    this.group_show = [];
    const group_ids: number[] = [];
    group_ids.push(this.promoSelected.group.id);
    while (group_ids.length > 0){
      const group_id = group_ids.pop();
      const group_find = this.groupes.find(group => group.id == group_id);
      if (group_find){
        this.group_show.push(group_find);
        const groups_temps = this.groupes.filter(group => group.id_group_parent == group_find.id);
        if (groups_temps.length > 0){
          for (let group of groups_temps){
            group_ids.push(group.id);
          }
        }
      }
    }
  }

  /*
      @function eventClicked
      @param event: any
      @desc: event clicked and open modal choice
  */
  eventClicked(event: any) {
    this.eventSelectionne = event;
    Promise.all([this.loadEventStart(this.eventSelectionne), this.loadEventEnd(this.eventSelectionne)])
      .then(([loadedEventStart, loadedEventEnd]) => {
        this.updateDateStart(loadedEventStart);
        this.updateDateEnd(loadedEventEnd);
        this.courseForEdit = this.getCourseByEventId(this.eventSelectionne.event.id)!;
        this.showModalChoice = true; // TODO : Fix le modal qui apparait a chaque drag sur firefox
      }
    );
  }

  /*
      @function loadEventStart
      @param event: any
      @return Promise<Date>
      @desc: load event start
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
      @param event: any
      @return Promise<Date>
      @desc: load event end
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
      @function eventTimesChanged
      @param event: any
      @desc: event times changed and update course
  */
  eventTimesChanged(event: any) {
    if (!this.brouillon) {
      this.brouillon = true;
      this.toastr.warning("Appuyez sur publier pour valider vos changements");
    }

    let course_find = this.courses.find(course => course.id == event.event.id);
    if (!course_find){return;}

    let start_time_initial = course_find.start_time;
    let end_time_initial = course_find.end_time;

    // Récupérer l'heure et les minutes de event.newStart
    let heuresDebut = event.newStart.getHours();
    let minutesDebut = event.newStart.getMinutes();

    // Récupérer l'heure et les minutes de event.newEnd
    let heuresFin = event.newEnd.getHours();
    let minutesFin = event.newEnd.getMinutes();

    // Comparer les heures et ajuster si nécessaire
    if (heuresDebut < 8 || (heuresDebut === 8 && minutesDebut < 0)) {
      event.newStart.setHours(8, 0); // Mettre l'heure de début à 8h00
    }

    if (heuresFin > 19 || (heuresFin === 19 && minutesFin > 0)) {
      event.newEnd.setHours(19, 0); // Mettre l'heure de fin à 19h00
    }

    course_find.start_time = event.newStart;
    course_find.end_time = event.newEnd;

    const event_backup = this.events.find(event => event.id == course_find!.id);

    this.events = this.events.filter((event) => event.id !== course_find!.id);
    this.addEvent(course_find);

    this.courseService.updateCourse(course_find).subscribe({
      next: course => {
        if ((course as any).status === 201) {
          this.toastr.warning('Ce professeur a déjà cours sur cette plage', 'Warning', { timeOut: 2000 });
        }
        this.courses.filter((course) => course.id !== course_find!.id);
        this.events = this.events.filter((event) => event.id !== course_find!.id);
        this.addCourse(course);
      },
      error: response => {
        if (response.status === 201) {
          this.toastr.warning('Ce professeur a déjà cours sur cette plage', 'Warning', { timeOut: 2000 });
        } else {
          course_find!.start_time = start_time_initial;
          course_find!.end_time = end_time_initial;
          this.events = this.events.filter((event) => event.id !== course_find!.id);
          this.events.push(event_backup!);
          this.toastr.error(response.error.error, 'Erreur', { timeOut: 2000 });
        }
      }
    });
  }

  /*
      @function endTimeChanged
      @param newEvent: any
      @param ancienneDate: string
      @desc: end time changed
  */
  endTimeChanged(newEvent: any, ancienneDate: string) {
    newEvent.event.end = Date.parse(ancienneDate);
    this.refresh.next();
    this.updateDateEnd(newEvent.event.end);
  }

  /*
      @function startTimeChanged
      @param newEvent: any
      @param ancienneDate: string
      @desc: start time changed
  */
  startTimeChanged(newEvent: any, ancienneDate: string) {
    newEvent.event.start = Date.parse(ancienneDate);
    this.refresh.next();
    this.updateDateStart(newEvent.event.start);
  }

  /*
      @function updateDateStart
      @param date: Date
      @desc: update date start
  */
  updateDateStart(date: Date) {
    this.eventSelectionne.event.start = date;
  }

  /*
      @function updateDateEnd
      @param date: Date
      @desc: update date end
  */
  updateDateEnd(date: Date) {
    this.eventSelectionne.event.end = date;
  }

  /*
      @function supprimerCours
      @param event: any
      @desc: delete course from event
  */
  supprimerCours(event: any){
    this.events.splice(this.getIndex(event), 1);
    this.refresh.next();
  }

  /*
      @function getCourseByEventId
      @param eventId: number
      @return Course
      @desc: get course by event id
  */
  getCourseByEventId(eventId: number) {
    return this.courses.find(course => course.id == eventId);
  }

  /*
      @function getRessourcesNameByInitial
      @param initial_resource: string
      @return string
      @desc: get ressources name by initial resource
  */
  getRessourcesNameByInitial(initial_resource: string) {
    return this.ressources.find(resource => resource.initial == initial_resource)?.name;
  }

  /*
      @function getRessourcesByInitial
      @param initial_resource: string
      @return Resource
      @desc: get ressources by initial resource
  */
  getRessourcesByInitial(initial_resource: string) {
    return this.ressources.find(resource => resource.initial == initial_resource);
  }


  /*
      @function getTimeString
      @param date: Date
      @return string
      @desc: get time string from date
  */
  getTimeString(date: Date) {
    return this.datePipe.transform(date, 'HH:mm');
  }


  /*
      @function getInitialTeacher
      @param id: number
      @return string
      @desc: get initial teacher
  */
  getInitialTeacher(id: number) {
    let id_teacher =  this.courses.find(course => course.id == id)?.id_enseignant;
    let teacher = this.teachers.find(teacher => teacher.id == id_teacher);
    return teacher? teacher.staff.initial : "";
  }


  /*
      @function publishCourse
      @desc: publish course
  */
  publishCourse(){
    this.courseService.publishCourses().subscribe({
      next:() => {
        this.toastr.success('Les cours ont été publiés', 'Succès',{timeOut: 1500,});
        this.loadEvents();
        this.brouillon = false;
      },
      error: error => {
        this.toastr.error(error, 'Erreur',{timeOut: 2000});
      }
    });
  }

  /*
      @function cancelCourse
      @desc: cancel course
  */
  cancelCourse(){
    this.courseService.cancelCourses().subscribe({
      next:() => {
        this.toastr.success('Les cours ont été annulés', 'Succès',{timeOut: 1500});
        this.loadEvents();
        this.brouillon = false;
      },
      error: error => {
        this.toastr.error(error, 'Erreur',{timeOut: 2000});
      }
    });
  }


  /*
      @function generateWeekDays
      @return Date[]
      @desc: generate week days
  */
  generateWeekDays(): Date[] {
    let displayedDates: Date[] = [];
    const start: Date = startOfWeek(this.viewDate, { weekStartsOn: DAYS_OF_WEEK.MONDAY });
    for (let i = 0; i < 7; i++) {
      displayedDates.push(addDays(start, i));
    }
    return displayedDates;
  }

  /*
      @function weekChanged
      @desc: week changed
  */
  weekChanged() {
    this.loadEvents();
    this.generateWeekDays();
  }

  /*
      @function receiveArray
      @param arrayData: Course[]
      @desc: receive array and set courses to paste
  */
  receiveArray(arrayData: Course[]): void {
    this.coursesToPaste = arrayData;
  }

  paste() {
    // console.log("Courses to paste", this.coursesToPaste);
  }

  /*
      @function setPasteEnable
      @param bool: boolean
      @desc: set paste enable to bool
  */
  setPasteEnable(bool: boolean){
    this.pasteEnable = bool;
  }

  /*
      @function onChangeSelectedDays
      @param selectedDays: any
      @desc: on change selected days set selected days
  */
  onChangeSelectedDays(selectedDays: any) {
    this.selectedDays = selectedDays;
  }

  /*
      @function closeModalChoice
      @desc: close modal choice
  */
  closeModalChoice(){
    this.showModalChoice = false;
    this.courseForEdit = null;
  }

  /*
      @function disablePreventDefault
      @param event: any
      @desc: disable prevent default event
  */
  disablePreventDefault(event: any){
    event.preventDefault();
  }

  /*
      @function redirectToLogout
      @param event: any
      @desc: redirect to logout
  */
  redirectToLogout(event: any){
    this.disablePreventDefault(event);
    window.location.href = "/logout";
  }
}
