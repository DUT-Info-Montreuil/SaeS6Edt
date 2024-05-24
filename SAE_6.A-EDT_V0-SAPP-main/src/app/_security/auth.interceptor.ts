import { Injectable } from '@angular/core'
import { HttpRequest, HttpHandler, HttpEvent, HttpInterceptor, HttpErrorResponse } from '@angular/common/http'
import { Observable, throwError } from 'rxjs'
import { catchError } from 'rxjs/operators'
import { EventBusService } from '../_shared/event-bus.service'
import { EventData } from '../_shared/event.class'
import { StorageService } from './storage.service'
import { Router } from '@angular/router'

const TOKEN_HEADER_KEY = 'Authorization';
const BEARER_TOKEN_HEADER_KEY = 'Bearer';

@Injectable()
export class AuthInterceptor implements HttpInterceptor {

  constructor(
    private storageService: StorageService,
    private eventBusService: EventBusService,
    private router: Router
  ) {}


  /*
      @function intercept
      @param req: HttpRequest<any>
      @param next: HttpHandler
      @return Observable<HttpEvent<Object>>
      @desc: intercept all request and add token in header
  */
  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<Object>> {
    let authReq = req
    const token = this.storageService.getToken()
    if (token != null && !authReq.url.includes('auth/login')    ) {
      if (this.storageService.isTokenExpired(token)) {
        this.eventBusService.emit(new EventData('unauthorized', null));
      } 
    }
    if (token) {
      authReq = authReq.clone({
        setHeaders: {
          [TOKEN_HEADER_KEY]: BEARER_TOKEN_HEADER_KEY + " " + token
        }
      });
    }
    return next.handle(authReq).pipe(catchError(error  => {
        if (error instanceof HttpErrorResponse && !authReq.url.includes('auth/login') && error.status === 401) {
            this.eventBusService.emit(new EventData('logout', null))
            this.router.navigate(['/login']); // Ajoutez le chemin de la page de déconnexion
        }
        return throwError(() => error)
    }));
  }
  

  /*
      @function getCookie
      @param name: string
      @return string | null
      @desc: get cookie by name
  */
  private getCookie(name: string): string | null {
    const match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
    return match ? decodeURIComponent(match[2]) : null;
  }
}
