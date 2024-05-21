import { DatePipe, registerLocaleData } from '@angular/common';
import { HTTP_INTERCEPTORS, HttpClientModule } from '@angular/common/http';
import localeFr from '@angular/common/locales/fr';
import { NgModule } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MatDialogModule } from '@angular/material/dialog';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { CalendarDateFormatter, CalendarModule, CalendarNativeDateFormatter, DateAdapter, DateFormatterParams } from 'angular-calendar';
import { ToastrModule } from 'ngx-toastr';
import { GeneralModule } from './_component/general/general.module';
import { momentAdapterFactory } from './_component/respEdt/calendar-week/week-calendar.component';
import { EdtModule } from './_component/respEdt/edt.module';
import { ElevesGroupesComponent } from './_component/respEdt/eleves-groupes/eleves-groupes.component';
import { FormsComponent } from './_component/respEdt/forms/forms.component';
import { AddModalEleveComponent } from './_component/respEdt/modals/add-modal-eleve/add-modal-eleve.component';
import { AddModalPromoComponent } from './_component/respEdt/modals/add-modal-promo/add-modal-promo.component';
import { CsvEleveModalComponent } from './_component/respEdt/modals/csv-eleve-modal/csv-eleve-modal.component';
import { ModifModalGroupComponent } from './_component/respEdt/modals/modif-modal-group/modif-modal-group.component';
import { TeacherModule } from './_component/teacher/teacher.module';
import { UsersModule } from './_component/user/user.module';
import { AuthInterceptor } from './_security/auth.interceptor';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { FilterPipe } from './pipes/filter.pipe';

registerLocaleData(localeFr, 'fr');

class CustomDateFormater extends CalendarNativeDateFormatter {

  public override dayViewHour({ date, locale }: DateFormatterParams): string {
      return new Intl.DateTimeFormat(locale, {hour: 'numeric', minute:'numeric'}).format(date);
  }
}

@NgModule({
  declarations: [
    AppComponent,
    FormsComponent,
    FilterPipe,
    ElevesGroupesComponent,
    ModifModalGroupComponent,
    AddModalEleveComponent,
    CsvEleveModalComponent,
    AddModalPromoComponent
  ],
  imports: [
    BrowserAnimationsModule,
    MatDialogModule,
    ToastrModule.forRoot({
      positionClass: 'toast-bottom-center',
      progressBar: true,
    }),
    BrowserModule,
    AppRoutingModule,
    CalendarModule.forRoot({ provide: DateAdapter, useFactory: momentAdapterFactory }),
    ReactiveFormsModule,
    FormsModule,
    HttpClientModule,
    UsersModule,
    EdtModule,
    GeneralModule,
    TeacherModule
  ],
  providers: [
    FormsComponent,
    DatePipe,
    {provide: CalendarDateFormatter, useClass:CustomDateFormater},
    HttpClientModule,
    FormsModule,
    { provide: HTTP_INTERCEPTORS, useClass: AuthInterceptor, multi: true }

  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
