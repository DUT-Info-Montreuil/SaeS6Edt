import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, Subject, retry } from 'rxjs';
import { UtilsService } from './utils.service';

@Injectable({
    providedIn: 'root'
})

export class UserGroupService {

    constructor(private http: HttpClient, private utilsService: UtilsService) { }

    private userGroupeRefreshSource = new Subject<void>();
    userGroupeRefresh$ = this.userGroupeRefreshSource.asObservable();


    /*
        @function notifyUserGroupRefresh
        @return void
        @desc: notify all subscribers that a user group has been updated
    */
    notifyUserGroupRefresh() {
        this.userGroupeRefreshSource.next();
    }


    /*
        @function addStudentToGroup
        @param idStudent: number
        @param idGroupe: number
        @return Observable<any>
        @desc: add a student to a group
    */
    addStudentToGroup(idStudent: number, idGroupe: number): Observable<any> {
        let url = `${this.utilsService.getEndPoint().apiUrl}/usergroupe/addGroupeEtudiant`;
        const requestData = {
            idStudent: idStudent,
            idGroupe: idGroupe
        };
        const requestBody = JSON.stringify(requestData);
        const headers = new HttpHeaders({
            'Content-Type': 'application/json'
        });
        return this.http.post<any>(url, requestBody, { headers: headers })
            .pipe(
                retry(1)
            );
    }


    /*
        @function deleteUserFromGroup
        @param idStudent: number
        @return Observable<any>
        @desc: delete a student from a group
    */
    deleteUserFromGroup(idStudent: number): Observable<any> {
        let url = `${this.utilsService.getEndPoint().apiUrl}/usergroupe/delete/${idStudent}`;
        return this.http.delete<any>(url, this.utilsService.getJsonHeader())
        .pipe(
            retry(1)
        );
    }


    /*
        @function getStudentsFromGroup
        @param idGroup: number
        @return Observable<any>
        @desc: get all students from a group
    */
    getStudentsFromGroup(idGroup: number): Observable<any> {
        let url = `${this.utilsService.getEndPoint().apiUrl}/usergroupe/groupe/${idGroup}`;
        return this.http.get<any>(url, this.utilsService.getJsonHeader())
        .pipe(
            retry(1)
        );
    }


    /*
        @function modifyGroupStudent
        @param idStudent: number
        @param newIdGroupe: number
        @param idGroupe: number
        @return Observable<any>
        @desc: modify a student from a group
    */
    modifyGroupStudent(idStudent: number, newIdGroupe: number, idGroupe: number): Observable<any> {
        let url = `${this.utilsService.getEndPoint().apiUrl}/usergroupe/modify/${idStudent}/${newIdGroupe}/${idGroupe}`;
        return this.http.put<any>(url, this.utilsService.getJsonHeader())
        .pipe(
            retry(1)
        );
    }


    /*
        @function migratePromotion
        @param idAncPromo: number
        @param idNvPromo: number
        @return Observable<any>
        @desc: migrate a promotion
    */
    migratePromotion(idAncPromo:number, idNvPromo: number): Observable<any> {
        let url = `${this.utilsService.getEndPoint().apiUrl}/usergroupe/migrate`;

        const body = {
            idAncPromo: idAncPromo,
            idNvPromo: idNvPromo,
        };

        return this.http.post<any>(url, body, this.utilsService.getJsonHeader())
        .pipe(
            retry(1)
        );
    }
}