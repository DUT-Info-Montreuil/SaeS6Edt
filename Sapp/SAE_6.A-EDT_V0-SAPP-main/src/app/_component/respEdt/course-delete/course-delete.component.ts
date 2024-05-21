import { Component, EventEmitter, Input, Output } from '@angular/core';
import { Course } from '../../../_model/entity/course.model';
import { CourseService } from 'src/app/_service/course.service';
import { ToastrService } from 'ngx-toastr';
import { WeekCalendarComponent } from '../calendar-week/week-calendar.component';

@Component({
  selector: 'course-delete',
  templateUrl: './course-delete.component.html',
  styleUrls: ['./course-delete.component.scss']
})

export class CourseDeleteComponent {
  @Input() course: Course;
  @Output() closeModal: EventEmitter<void> = new EventEmitter<void>();
  @Output() removeEvent: EventEmitter<Course> = new EventEmitter<Course>();

  constructor(
    private courseService: CourseService,
    private toastr: ToastrService,
    private weekComp: WeekCalendarComponent
  ) {}
  
  /*
    @function deleteCourse
    @desc: delete course and emit event to parent
  */
  deleteCourse() {
    this.courseService.deleteCourse(this.course).subscribe({
      next: course => {
        this.removeEvent.emit(course);
        this.closeModal.emit();
        this.toastr.success('Le cours a été supprimé', 'Cours supprimé', { timeOut: 1500 });
        this.weekComp.changeBrouillonValue();
      },
      error: response => {
        this.toastr.error(response.error.error, 'Erreur', { timeOut: 2000 });
      }
    });
  }
}