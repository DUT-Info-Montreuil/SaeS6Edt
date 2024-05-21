import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { FormBuilder, FormGroup, Validators, AbstractControl } from '@angular/forms';
import { Teacher } from '../../../_model/entity/teacher.model';
import { Course } from '../../../_model/entity/course.model';
import { Resource } from '../../../_model/entity/resource.model';
import { Group } from '../../../_model/entity/group.model';

import { Room } from 'src/app/_model/entity/room.model';
import { CourseService } from 'src/app/_service/course.service';
import { ToastrService } from 'ngx-toastr';


@Component({
  selector: 'course-edit',
  templateUrl: './course-edit.component.html',
  styleUrls: ['./course-edit.component.scss']
})

export class CourseEditComponent implements OnInit{

    courseForm: FormGroup;
    @Input() teachers: Teacher[];
    @Input() salles: Room[];
    @Input() groupes: Group[];
    @Input() resources: Resource[];
    @Input() course: Course;
    @Input() courses: Course[];

    @Output() courseEvent: EventEmitter<Course> = new EventEmitter<Course>();
    @Output() closeModal: EventEmitter<void> = new EventEmitter<void>();
    @Output() removeEvent: EventEmitter<Course> = new EventEmitter<Course>();
    @Output() refresh: EventEmitter<void> = new EventEmitter<void>();

    showModalDuplicate: boolean;
    selectedGroups: number[] = [];

    dateStartIf: Date;
    dateEndIf: Date;

    constructor(
        private formBuilder: FormBuilder,
        private courseService: CourseService,
        private toastr: ToastrService
    ) {}

    /*
        @function ngOnInit
        @desc: on init form
    */
    ngOnInit() {
        this.initializeForm();
    }

    /*
        @function initializeForm
        @desc: initialize form with course data
    */
    initializeForm() {
        let start_time = new Date(this.course.start_time);
        let end_time = new Date(this.course.end_time);

        const date = start_time.toISOString().split('T')[0];

        const start = start_time.toTimeString().split(' ')[0];

        const end = end_time.toTimeString().split(' ')[0];

        this.courseForm = this.formBuilder.group({
            id_enseignant: [this.course.id_enseignant?this.course.id_enseignant:"", []],
            initial_ressource: [this.course.initial_ressource, [
                Validators.required,
                this.validateSelect
            ]],
            id_group: [this.course.id_group, [
                Validators.required,
                this.validateSelect
            ]],
            name_salle: [this.course.name_salle?this.course.name_salle:"", []],
            evaluation: [this.course.evaluation,[Validators.required]],
            date: [date, [Validators.required]],
            start: [start, [Validators.required]],
            end: [end, [Validators.required]],  
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
        @desc: submit form and send course
    */
    onSubmit(){
        if (this.courseForm.invalid) {
            return;
        }
        const course_edit: Course = new Course();
        Object.assign(course_edit, this.course);
        Object.assign(course_edit, this.courseForm.value);
        
        course_edit.start_time = this.createDateObject(this.courseForm.value.date, this.courseForm.value.start);
        course_edit.end_time = this.createDateObject(this.courseForm.value.date, this.courseForm.value.end);

        this.dateStartIf = this.createDateObject(this.courseForm.value.date, "8:00");
        this.dateEndIf = this.createDateObject(this.courseForm.value.date, "18:00");

        if (course_edit.start_time < this.dateStartIf){
            this.toastr.error("Les cours ne peuvent pas commencer avant 8h");
        } else if (course_edit.end_time > this.dateEndIf){
            this.toastr.error("Les cours ne peuvent pas finir après 18h");
        } else {
            this.courseService.updateCourse(course_edit).subscribe({
                next: course => {
                    this.closeModal.emit();
                    this.removeEvent.emit(course_edit);
                    this.courseEvent.emit(course);
                    this.toastr.success('Le cours a été modifié', 'Cours modifié',{timeOut: 1500});
                },
                error: response => {
                    console.log(response);
                    this.toastr.error(response.error.error, 'Erreur',{timeOut: 2000});
                }
            });
        }
    }
}