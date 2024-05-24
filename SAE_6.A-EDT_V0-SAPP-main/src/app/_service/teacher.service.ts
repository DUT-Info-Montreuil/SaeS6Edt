import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, Subject, retry } from 'rxjs';
import { Teacher } from '../_model/entity/teacher.model';
import { UtilsService } from './utils.service';

@Injectable({
    providedIn: 'root'
})
export class TeacherService {

    constructor(private http: HttpClient, private utilsService: UtilsService) { }

    private profRefreshSource = new Subject<void>();
    profRefresh$ = this.profRefreshSource.asObservable();


    /*
        @function notifyProfRefresh
        @return void
        @desc: notify all subscribers that a teacher has been updated
    */
    notifyProfRefresh(){
        this.profRefreshSource.next();
    }



    /*
        @function getTeachers
        @return Observable<Teacher[]>
        @desc: get all teachers
    */
    getTeachers(): Observable<Teacher[]> {
        let url = `${this.utilsService.getEndPoint().apiUrl}/teachers`;
        return this.http.get<Teacher[]>(url, this.utilsService.getJsonHeader())
        .pipe(
            retry(1)
        );
    }


    /*
        @function addTeacher
        @param teacher: Teacher
        @return Observable<Teacher>
        @desc: add a teacher
    */
    addTeacher(teacher: Teacher): Observable<Teacher> {

        const teacherData = this.parseAddTeacher(teacher);

        let url = `${this.utilsService.getEndPoint().apiUrl}/teacher`;
        return this.http.post<Teacher>(url, teacherData, this.utilsService.getJsonHeader())
        .pipe(
            retry(1)
        );
    }

    /*
        @function addTeacherCSV
        @param csv: any
        @return Observable<any>
        @desc: add multiple teachers from a CSV file
    */
    addTeacherCSV(csv: any): Observable<any> {
        let url = `${this.utilsService.getEndPoint().apiUrl}/teachers/csv`;
        return this.http.post<any>(url, csv, this.utilsService.getJsonHeader())
        .pipe(
            retry(1)
        );
    }

    /*
        @function updateTeacher
        @param teacher: Teacher
        @return Observable<Teacher>
        @desc: update a teacher
    */
    updateTeacher(teacher: Teacher): Observable<Teacher> {

        const teacherData = this.parseUpdateTeacher(teacher);
        
        let url = `${this.utilsService.getEndPoint().apiUrl}/teacher/${teacher.id}`;
        return this.http.put<Teacher>(url, teacherData, this.utilsService.getJsonHeader())
        .pipe(
            retry(1)
        );
    }

    /*
        @function getTeacher
        @param id: number
        @return Observable<Teacher>
        @desc: get a teacher
    */
    getTeacher(id: number): Observable<Teacher> {
        let url = `${this.utilsService.getEndPoint().apiUrl}/teacher/${id}`;
        return this.http.get<Teacher>(url, this.utilsService.getJsonHeader())
        .pipe(
            retry(1)
        );
    }


    /*
        @function deleteTeacher
        @param id: number
        @return Observable<Teacher>
        @desc: delete a teacher
    */
    deleteTeacher(id: number): Observable<Teacher> {
        let url = `${this.utilsService.getEndPoint().apiUrl}/teacher/${id}`;
        return this.http.delete<Teacher>(url, this.utilsService.getJsonHeader())
        .pipe(
            retry(1)
        );
    }


    /*
        @function parseUpdateTeacher
        @param teacher: Teacher
        @return any
        @desc: parse a teacher to fit the API
    */

    parseUpdateTeacher(teacher: Teacher): any {
        return {
            "name": teacher.staff.user.name,
            "lastname": teacher.staff.user.lastname,
            "activated": teacher.activated
            // "password": teacher.staff.user.password!,
            // "username": teacher.staff.user.username,
        }
    }


    /*
        @function parseAddTeacher
        @param teacher: Teacher
        @return any
        @desc: parse a teacher to fit the API
    */
    parseAddTeacher(teacher: Teacher): any {
        return {
            "name": teacher.staff.user.name,
            "lastname": teacher.staff.user.lastname,
            "password": teacher.staff.user.password!,
            "username": teacher.staff.user.username,
        }
    }
}
