import { CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { Calendar } from './calendar/calendar.component';
import { RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';
import { UsersModule } from '../user/user.module';
import { EdtModule } from '../respEdt/edt.module';
import { TeacherModule } from '../teacher/teacher.module';
import { ChangePasswdComponent } from './change-passwd/change-passwd.component';
import { ReactiveFormsModule } from '@angular/forms';


@NgModule({
  declarations: [
    Calendar,
    ChangePasswdComponent // Assurez-vous que le composant est déclaré ici
  ],
  imports: [
    RouterModule,
    CommonModule,
    UsersModule,
    EdtModule,
    TeacherModule,
    ReactiveFormsModule
  ],
  providers: [],
  exports: [
    ChangePasswdComponent // Exportez le composant ici si vous voulez l'utiliser ailleurs
  ],
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})

export class GeneralModule { }
