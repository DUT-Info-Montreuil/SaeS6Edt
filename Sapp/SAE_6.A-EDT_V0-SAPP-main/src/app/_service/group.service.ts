import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, Subject, retry } from 'rxjs';
import { Group } from '../_model/entity/group.model';
import { UtilsService } from './utils.service';

@Injectable({
    providedIn: 'root'
})
export class GroupService {

    constructor(private http: HttpClient, private utilsService: UtilsService) { }

    private groupeRefreshSource = new Subject<void>();
    groupeRefresh$ = this.groupeRefreshSource.asObservable();


    /*
        @function notifyGroupRefresh
        @return void
        @desc: notify all subscribers that a group has been updated
    */
    notifyGroupRefresh() {
        this.groupeRefreshSource.next();
    }



    /*
        @function getGroups
        @return Observable<Group[]>
        @desc: get all groups
    */
    getGroups(): Observable<Group[]> {
        let url = `${this.utilsService.getEndPoint().apiUrl}/groupes`;
        return this.http.get<Group[]>(url, this.utilsService.getJsonHeader())
        .pipe(
            retry(1)
        );
    }

    /*
        @function addGroup
        @param group: Group
        @return Observable<Group>
        @desc: add a group
    */
    addGroup(group: Group): Observable<Group> {
        let url = `${this.utilsService.getEndPoint().apiUrl}/groupe`;
        return this.http.post<Group>(url, group, this.utilsService.getJsonHeader())
        .pipe(
            retry(1)
        );
    }

    /*
        @function updateGroup
        @param group: Group
        @return Observable<Group>
        @desc: update a group
    */
    updateGroup(group: Group): Observable<Group> {
        let url = `${this.utilsService.getEndPoint().apiUrl}/groupe/${group.id}`;
        return this.http.put<Group>(url, group, this.utilsService.getJsonHeader())
        .pipe(
            retry(1)
        );
    }

    /*
        @function getGroup
        @param id: number
        @return Observable<Group>
        @desc: get a group
    */
    getGroup(id: number): Observable<Group> {
        let url = `${this.utilsService.getEndPoint().apiUrl}/groupe/${id}`;
        return this.http.get<Group>(url, this.utilsService.getJsonHeader())
        .pipe(
            retry(1)
        );
    }

    /*
        @function getTreeGroup
        @param id: number
        @return Observable<Group>
        @desc: get a group with his childs and parents
    */
    getTreeGroup(id: number): Observable<Group> {
        let url = `${this.utilsService.getEndPoint().apiUrl}/groupe/tree/${id}`;
        return this.http.get<Group>(url, this.utilsService.getJsonHeader())
        .pipe(
            retry(1)
        );
    }

    /*
        @function getChildsGroup
        @param id: number
        @return Observable<Group>
        @desc: get all childs of a group
    */
    getChildsGroup(id: number): Observable<Group> {
        let url = `${this.utilsService.getEndPoint().apiUrl}/groupe/childs/${id}`;
        return this.http.get<Group>(url, this.utilsService.getJsonHeader())
        .pipe(
            retry(1)
        );
    }

    /*
        @function deleteGroup
        @param id: number
        @return Observable<Group>
        @desc: delete a group
    */
    deleteGroup(id: number): Observable<Group> {
        let url = `${this.utilsService.getEndPoint().apiUrl}/groupe/${id}`;
        return this.http.delete<Group>(url, this.utilsService.getJsonHeader())
        .pipe(
            retry(1)
        );
    }
}
