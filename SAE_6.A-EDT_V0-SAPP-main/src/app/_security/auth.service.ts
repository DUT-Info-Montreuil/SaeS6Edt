import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, catchError, map, of, retry } from 'rxjs';
import { UtilsService } from '../_service/utils.service';
import { StorageService } from './storage.service';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  public user: Observable<string | null>;

  constructor(
    private http: HttpClient,
    private utilsService: UtilsService,
    private storageService: StorageService
  ) {}

  /*
      @function logoutUser
      @desc: logout user
  */
  logoutUser() {
    this.storageService.signOut();
    window.location.href = '/login';
  }

  /*
      @function login
      @param username: string
      @param password: string
      @return Observable<any>
      @desc: login user
  */
  login(username: string, password: string): Observable<any> {
    const url = `${this.utilsService.getEndPoint().apiUrl}/auth/login`;
    return this.http
      .post(url, { username, password }, this.utilsService.getJsonHeader())
      .pipe(retry(1));
  }

  /*
      @function logout
      @return Observable<any>
      @desc: logout user
  */
  logout(): Observable<any> {
    const url = `${this.utilsService.getEndPoint().apiUrl}/logout`;
    return this.http.get(url, this.utilsService.getJsonHeader()).pipe(retry(1));
  }

  getRole(): Observable<string | null> {
    const url = `${this.utilsService.getEndPoint().apiUrl}/auth/role`;
    return this.http.get(url, this.utilsService.getJsonHeader()).pipe(
      map((response: any) => response.role),
      catchError((error: any) => {
        console.error(
          "Erreur lors de la récupération du rôle de l'utilisateur:",
          error
        );
        return of(null);
      })
    );
  }

  /*
      @function changePasswd
      @return Observable<any>
      @desc: change password of a user
  */
  changePasswd(username: string, password: string, newPasswd: string): Observable<any>{
    const url = `${this.utilsService.getEndPoint().apiUrl}/auth/changepasswd`;
    return this.http.put(url, {username, password, newPasswd}, this.utilsService.getJsonHeader())
    .pipe(
      retry(1)
    );
  }

  /*
    @function verifMdp
    @return Observable<any>
    @desc: verify user password
  */
  verifyPasswd(username: string, password: string){
    const url = `${this.utilsService.getEndPoint().apiUrl}/auth/verifpasswd`;
    return this.http.post(url, {username, password}, this.utilsService.getJsonHeader())
    .pipe(
      retry(1)
    );
  }
}
