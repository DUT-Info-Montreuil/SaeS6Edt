import { Injectable } from '@angular/core'
import { AuthResponse } from '../_model/fonctional/auth-response.model'
import { User } from '../_model/entity/user.model'
import { UserService } from '../_service/user.service'

const TOKEN_KEY = 'auth-token';
const USER_KEY = 'auth-user';
const ROLE_KEY = 'auth-role';


@Injectable({
  providedIn: 'root'
})
export class StorageService {

  user: User
  
  constructor(private userService: UserService) {}

  

  /*
      @function signOut
      @desc: sign out user
  */
  signOut(): void {
    window.localStorage.clear()
  }

  /*
      @function saveToken
      @param token: string
      @desc: save token in local storage
  */
  public saveToken(token: string): void {
    window.localStorage.removeItem(TOKEN_KEY);
    window.localStorage.setItem(TOKEN_KEY, token);
  }

  /*
      @function getToken
      @return string | null
      @desc: get token from local storage
  */
  public getToken(): string | null {
    return window.localStorage.getItem(TOKEN_KEY);
  }


  /*
      @function saveResponse
      @param auth: AuthResponse
      @desc: save response in local storage
  */
  public saveResponse(auth: AuthResponse): void {
    this.saveToken(auth.access_token);
  }

  
  /*
      @function IsLoggedIn
      @return boolean
      @desc: check if user is logged in
  */
  public isLoggedIn(): boolean {
    if (this.getToken()) {
      return true;
    }
    return false;
  }

  /*
      @function isTokensValid
      @return boolean
      @desc: check if tokens are valid
  */
  isTokensValid(): boolean {
    if(this.getToken() == undefined || this.getToken() == null) { return false; }
    return this.isTokenExpired(this.getToken());
  }
  
  /*
      @function getRoleList
      @return string[]
      @desc: get role list
  */
  getRoleList(): string[] {
    return ['ROLE_STUDENT', 'ROLE_TEACHER', 'ROLE_RESP_EDT'];
  }

  /*
      @function isTokenExpired
      @param token: string | null
      @return boolean
      @desc: check if token is expired
  */
  isTokenExpired(token: string | null): boolean {
    const tokenData = this.decodeToken(token);
    if (!tokenData) {
      return true; // Le token est invalide
    }
    const currentTime = Date.now() / 1000;// Temps actuel en secondes
    return tokenData.exp < currentTime;
  }

  /*
      @function decodeToken
      @param token: string | null
      @return any
      @desc: decode token
  */
  private decodeToken(token: string | null): any {
    try {
      const tokenPayload = JSON.parse(window.atob(token!.split('.')[1]));
      return tokenPayload;
    } catch (error) {
      return null;
    }
  }
}
