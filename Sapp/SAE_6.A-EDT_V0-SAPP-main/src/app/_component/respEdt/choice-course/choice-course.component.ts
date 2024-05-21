import { Component, EventEmitter, Input, NgZone, OnInit, Output } from '@angular/core';
import { Course } from 'src/app/_model/entity/course.model';
import { Group } from 'src/app/_model/entity/group.model';
import { Resource } from 'src/app/_model/entity/resource.model';
import { Room } from 'src/app/_model/entity/room.model';
import { Teacher } from 'src/app/_model/entity/teacher.model';

@Component({
  selector: 'choice-course',
  templateUrl: './choice-course.component.html',
  styleUrls: ['./choice-course.component.scss']
})
export class ChoiceCourseComponent implements OnInit {
  @Input() teachers: Teacher[];
  @Input() salles: Room[];
  @Input() groupes: Group[];
  @Input() resources: Resource[];
  @Input() course: Course;
  @Input() courses: Course[];
  @Output() courseEvent: EventEmitter<Course> = new EventEmitter<Course>();
  @Output() removeEvent: EventEmitter<Course> = new EventEmitter<Course>();
  @Output() refresh: EventEmitter<void> = new EventEmitter<void>();
  choice: string = 'edit';
  groupe_available: Group[] = [];
  @Output() closeModalEmitter: EventEmitter<void> = new EventEmitter<void>();

  constructor(private zone: NgZone) {}

  /*
    @function ngOnInit
    @desc: on init
  */
  ngOnInit() {
    this.getGroupAvailableForDuplicate();
  }

  /*
    @function closeModal
    @desc: close modal
  */
  closeModal() {
    this.closeModalEmitter.emit();
  }

  changeChoice(choice: string) {
    this.zone.run(() => {
      this.choice = choice;
    });
  }

  removeEventEmit(course: Course) {
    this.removeEvent.emit(course);
  }

  refreshEmit() {
    this.refresh.emit();
  }

  courseEventEmit(course: Course) {
    this.courseEvent.emit(course);
  }

  getGroupAvailableForDuplicate() {
    const course_same_time = this.courses.filter(course => {
      return (
        this.course.start_time >= course.start_time &&
        this.course.start_time < course.end_time ||
        this.course.end_time > course.start_time &&
        this.course.end_time <= course.end_time ||
        this.course.start_time <= course.start_time &&
        this.course.end_time >= course.end_time
      );
    });
    const group_unavailable: Group[] = [];
    course_same_time.forEach(course => {
      let current_group = this.groupes.find(group => group.id === course.id_group)!;

      if (!group_unavailable.find(group => group.id === current_group.id)) {
        group_unavailable.push(current_group);
        while (current_group.id_group_parent != null) {
          current_group = this.groupes.find(group => group.id === current_group.id_group_parent)!;
          if (!group_unavailable.find(group => group.id === current_group.id)) {
            group_unavailable.push(current_group);
          }
        }
      }

      let group_children: Group[] = this.groupes.filter(group => group.id_group_parent === course.id_group);
      while (group_children.length > 0) {
        const children_current = this.groupes.find(group => group.id === group_children[0].id)!;
        if (!group_unavailable.find(group => group.id === children_current.id)) {
          group_unavailable.push(children_current);
        }

        const other_children = this.groupes.filter(group => group.id_group_parent === children_current.id);
        group_children = group_children.concat(other_children);
        group_children.shift();
      }
    });
    this.groupe_available = this.groupes.filter(group => !group_unavailable.find(group_unavailable => group_unavailable.id === group.id));
  }
}