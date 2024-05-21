import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LoginComponent } from './_component/user/login/login.component';
import { FormsComponent } from './_component/respEdt/forms/forms.component';
import { WeekViewCalendarComponent } from './_component/user/calendar-week/week-view-calendar.component';
import { Calendar } from './_component/general/calendar/calendar.component';
import { LogoutComponent } from './_component/user/logout/logout.component';
import { ElevesGroupesComponent } from './_component/respEdt/eleves-groupes/eleves-groupes.component';
import { AdminGuard } from './_security/admin.guard';

const routes: Routes = [
  { path: '', component: Calendar },
  { path: 'login', component: LoginComponent },
  { path: 'logout', component: LogoutComponent },
  { path: 'ajout', component: FormsComponent, canActivate: [AdminGuard] },
  { path: 'user', component: WeekViewCalendarComponent },
  { path: 'groupes', component: ElevesGroupesComponent, canActivate: [AdminGuard] },
  { path: '**', redirectTo: '/', data: { error404: true } },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)], //RouterModule.forRoot(routes, { useHash: true })
  exports: [RouterModule],
})
export class AppRoutingModule {}
