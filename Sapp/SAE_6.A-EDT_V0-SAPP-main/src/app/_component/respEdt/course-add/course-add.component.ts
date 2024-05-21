import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { FormBuilder, FormGroup, Validators, AbstractControl } from '@angular/forms';
import { Teacher } from '../../../_model/entity/teacher.model';
import { Course } from '../../../_model/entity/course.model';
import { Resource } from '../../../_model/entity/resource.model';
import { Group } from '../../../_model/entity/group.model';
import { Room } from 'src/app/_model/entity/room.model';
import { CourseService } from 'src/app/_service/course.service';
import { ToastrService } from 'ngx-toastr';
import { WeekCalendarComponent } from '../calendar-week/week-calendar.component';

@Component({
  selector: 'course-add',
  templateUrl: './course-add.component.html',
  styleUrls: ['./course-add.component.scss']
})

export class CourseAddComponent implements OnInit {
  courseForm: FormGroup;
  @Input() teachers: Teacher[];
  @Input() salles: Room[];
  @Input() groupes: Group[];
  @Input() resources: Resource[];

  @Output() courseEvent: EventEmitter<Course> = new EventEmitter<Course>();
  @Output() closeModal: EventEmitter<void> = new EventEmitter<void>();

  dateStartIf: Date;
  dateEndIf: Date;

  constructor(
    private formBuilder: FormBuilder,
    private courseService: CourseService,
    private toastr: ToastrService,
    private weekComp: WeekCalendarComponent
  ) {}
  
  /*
    @function ngOnInit
    @desc: on init form
  */
  ngOnInit() {
    this.courseForm = this.formBuilder.group({
      id_enseignant: ['', []],
      initial_ressource: ['', [Validators.required, this.validateSelect]],
      id_group: ['', [Validators.required, this.validateSelect]],
      name_salle: [''],
      evaluation: [false, [Validators.required]],
      date: ['', [Validators.required]],
      start: ['', [Validators.required]],
      end: ['', [Validators.required]],  
    });
  }

  /*
    @function toggleEvaluation
    @desc: toggle evaluation value in form
  */
  toggleEvaluation() {
    this.courseForm.patchValue({
      evaluation: !this.courseForm.value.evaluation
    });
  }

  /*
    @function validateSelect
    @param control: AbstractControl
    @param object: any[]
    @desc: validate select value in form obligatory
  */
  validateSelect(control: AbstractControl, object: any[]): { [key: string]: boolean } | null {
    const selectedValue = control.value;
    if (!selectedValue) {
      return { 'required': true };
    }
    return null;
  }

  /*
    @function createDateObject
    @param dateString: string
    @param timeString: string
    @desc: create date object from string date and time
  */
  createDateObject(dateString: string, timeString: string): Date {
    const [year, month, day] = dateString.split('-').map(Number);
    const [hours, minutes] = timeString.split(':').map(Number);
    const dateObject = new Date(year, month - 1, day, hours, minutes);
    return dateObject;
  }

  /*
    @function onSubmit
    @desc: on submit form send course to parent and close modal
  */
  onSubmit() {
    if (this.courseForm.invalid) {
      return;
    }

    const course: Course = this.courseForm.value;
    course.start_time = this.createDateObject(this.courseForm.value.date, this.courseForm.value.start);
    course.end_time = this.createDateObject(this.courseForm.value.date, this.courseForm.value.end);

    this.dateStartIf = this.createDateObject(this.courseForm.value.date, "8:00");
    this.dateEndIf = this.createDateObject(this.courseForm.value.date, "18:00");

    if (course.start_time < this.dateStartIf){
      this.toastr.error("Les cours ne peuvent pas commencer avant 8h");
    } else if (course.end_time > this.dateEndIf){
      this.toastr.error("Les cours ne peuvent pas finir après 18h");
    } else {
      this.courseService.addCourse(course).subscribe({
        next: course => {
          this.courseEvent.emit(course);
          this.closeModalAdd();
          this.toastr.success('Cours ajouté', 'Succès',{timeOut: 1500});
          this.weekComp.changeBrouillonValue();
        },
        error: response => {
          console.log(response);
          this.toastr.error(response.error.error , 'Erreur',{timeOut: 2000});
        }
      });
    }
  }

  /*
    @function closeModalAdd
    @desc: close modal emit to parent
  */
  closeModalAdd() {
    this.closeModal.emit();
  }
}