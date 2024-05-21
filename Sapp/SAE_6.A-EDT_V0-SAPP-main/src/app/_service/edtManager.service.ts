import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, Subject, retry } from 'rxjs';
import { EdtManager } from '../_model/entity/edtManager.model';
import { Promotion } from '../_model/entity/promotion.model';
import { UtilsService } from './utils.service';

@Injectable({
    providedIn: 'root'
})
export class EdtManagerService {

    constructor(private http: HttpClient, private utilsService: UtilsService) { }

    private respRefreshSource = new Subject<void>();
    respRefresh$ = this.respRefreshSource.asObservable();


    /*
        @function notifyRespRefresh
        @return void
        @desc: notify all subscribers that a respEdt has been updated
    */
    notifyRespRefresh(){
        this.respRefreshSource.next();
    }

    /*
        @function getEdtManagers
        @return Observable<EdtManager[]>
        @desc: get all respEdt
    */

    getEdtManagers(): Observable<EdtManager[]> {
        let url = `${this.utilsService.getEndPoint().apiUrl}/responsables`;
        return this.http.get<EdtManager[]>(url, this.utilsService.getJsonHeader())
        .pipe(
            retry(1)
        );
      }

    /*
        @function addEdtManager
        @param edtManager: EdtManager
        @return Observable<EdtManager>
        @desc: add a respEdt
    */
    addEdtManager(edtManager: EdtManager): Observable<EdtManager> {
        let url = `${this.utilsService.getEndPoint().apiUrl}/responsable`;
        return this.http.post<EdtManager>(url, edtManager, this.utilsService.getJsonHeader())
        .pipe(
            retry(1)
        );
      }

    /*
        @function updateEdtManager
        @param edtManager: EdtManager
        @return Observable<EdtManager>
        @desc: update a respEdt
    */
    updateEdtManager(edtManager: EdtManager): Observable<EdtManager> {
        let url = `${this.utilsService.getEndPoint().apiUrl}/responsable/${edtManager.id}`;
        return this.http.put<EdtManager>(url, edtManager, this.utilsService.getJsonHeader())
        .pipe(
            retry(1)
        );
      }

        /*
            @function getEdtManager
            @param id: number
            @return Observable<EdtManager>
            @desc: get a respEdt
        */
    getEdtManager(id: number): Observable<EdtManager> {
        let url = `${this.utilsService.getEndPoint().apiUrl}/responsable/${id}`;
        return this.http.get<EdtManager>(url, this.utilsService.getJsonHeader())
        .pipe(
            retry(1)
        );
    }

    /*
        @function getPromoEdtManager
        @return Observable<Promotion[]>
        @desc: get all promotions for a respEdt
    */
    getPromoEdtManager(): Observable<Promotion[]> {
        let url = `${this.utilsService.getEndPoint().apiUrl}/responsable/promos`;
        return this.http.get<Promotion[]>(url, this.utilsService.getJsonHeader())
        .pipe(
            retry(1)
        );
    }

    /*
        @function deleteEdtManager
        @param id: number
        @return Observable<EdtManager>
        @desc: delete a respEdt
    */
    deleteEdtManager(id: number): Observable<EdtManager> {
        let url = `${this.utilsService.getEndPoint().apiUrl}/responsable/${id}`;
        return this.http.delete<EdtManager>(url, this.utilsService.getJsonHeader())
        .pipe(
            retry(1)
        );
    }

    /*
        @function parseEdtManager
        @param edtManager: EdtManager
        @return any
        @desc: parse a respEdt to send to API
    */
    parseEdtManager(edtManager: EdtManager): any {
        return {
            "name": edtManager.staff.user.name,
            "lastname": edtManager.staff.user.lastname,
            "password": edtManager.staff.user.password!,
            "username": edtManager.staff.user.username,
        }
    }
}
