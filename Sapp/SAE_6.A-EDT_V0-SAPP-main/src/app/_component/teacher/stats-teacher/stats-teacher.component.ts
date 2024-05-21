import { Component, EventEmitter, Output, Input } from '@angular/core';
import { CourseService } from 'src/app/_service/course.service';

@Component({
  selector: 'stats-teacher',
  templateUrl: './stats-teacher.component.html',
  styleUrls: ['./stats-teacher.component.scss']
})

export class StatsTeacherComponent {

  @Input() idTeacher: number;

  @Output() closeModal: EventEmitter<void> = new EventEmitter<void>();

  stats: any[] = [];

  constructor(private courseService : CourseService) { }

  /*
    @function ngOnInit
    @desc Initializes the component and retrieves statistics for the teacher from the course service
  */
  ngOnInit(): void {
      this.courseService.getStatsTeacher(this.idTeacher).subscribe((stats: any[]) => {
        this.stats = stats;
      });
  }
  
  /*
    @function closeModalStats
    @desc Emits an event to close the statistics modal
  */
  closeModalStats() {
      this.closeModal.emit();
  }
}
