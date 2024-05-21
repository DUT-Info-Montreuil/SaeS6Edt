import { HttpClient, HttpHeaders } from '@angular/common/http'
import { Injectable } from '@angular/core'
import { environment } from 'src/environments/environment.development'

@Injectable({
  providedIn: 'root'
})
export class UtilsService {

  constructor(
    private http: HttpClient) {}
  
  
  /*
      @function getEndPoint
      @return EndPoint
      @desc: get the endpoint according to environment
  */
  getEndPoint(): EndPoint {
    if (environment.production) {
         console.log("prod");
      return {
        apiUrl: environment.apiUrl,
      }
    } else {
              console.log("dev");
      return {
        apiUrl: environment.apiUrl,
      }
    }
  }

  getJsonHeader() {
    return {
      headers: new HttpHeaders({
        'Content-Type': 'application/json; charset=UTF-8',
      }),
      withCredentials: true
    }
  }


}

export class EndPoint {
  apiUrl: string
}
