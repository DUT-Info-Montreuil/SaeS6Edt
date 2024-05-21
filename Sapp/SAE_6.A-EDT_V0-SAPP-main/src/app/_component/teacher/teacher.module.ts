import { CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule } from '@angular/forms';
import { FormsModule } from '@angular/forms';

import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import { CalendarModule, DateAdapter } from 'angular-calendar';
import { WeekViewTeacherCalendarComponent, momentAdapterFactory } from './calendar-week/week-view-teacher-calendar.component';
import { StatsTeacherComponent } from './stats-teacher/stats-teacher.component';


@NgModule({
  declarations: [
    WeekViewTeacherCalendarComponent,
    StatsTeacherComponent
  ],
  imports: [
    RouterModule,
    CommonModule,
    ReactiveFormsModule,
    FormsModule,
    BrowserAnimationsModule,
    CalendarModule.forRoot({ provide: DateAdapter, useFactory: momentAdapterFactory })
  ],
  exports: [
    WeekViewTeacherCalendarComponent
  ],
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})

export class TeacherModule { }
