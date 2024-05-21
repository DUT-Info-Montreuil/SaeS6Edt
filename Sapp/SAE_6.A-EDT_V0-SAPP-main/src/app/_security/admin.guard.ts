import { Injectable } from '@angular/core';
import { AuthService } from './auth.service';
import { Observable, of } from 'rxjs';
import { Router } from '@angular/router';
import { map, catchError } from 'rxjs/operators';

@Injectable({
  providedIn: 'root',
})
export class AdminGuard {
  constructor(private authService: AuthService, private router: Router) {}

  canActivate(): Observable<boolean> {
    return this.authService.getRole().pipe(
      map((role) => {
        if (role !== 'ROLE_RESP_EDT') {
          this.router.navigate(['/erreur']);
          return false;
        }
        return true;
      }),
      catchError((error) => {
        console.error(
          "Erreur lors de la récupération du rôle de l'utilisateur:",
          error
        );
        this.router.navigate(['/erreur']);
        return of(false);
      })
    );
  }
}
