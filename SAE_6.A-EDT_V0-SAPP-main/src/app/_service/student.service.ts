import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, Subject, retry } from 'rxjs';
import { Student } from '../_model/entity/student.model';
import { UtilsService } from './utils.service';

@Injectable({
    providedIn: 'root'
})
export class StudentService {

    constructor(private http: HttpClient, private utilsService: UtilsService) { }

    private studentRefreshSource = new Subject<void>();
    studentRefresh$ = this.studentRefreshSource.asObservable();


    /*
        @function notifyStudentRefresh
        @return void
        @desc: notify all subscribers that a student has been updated
    */
    notifyStudentRefresh() {
        this.studentRefreshSource.next();
    }



    /*
        @function getStudents
        @return Observable<Student[]>
        @desc: get all students
    */
    getStudents(): Observable<Student[]> {
        let url = `${this.utilsService.getEndPoint().apiUrl}/students`;
        return this.http.get<Student[]>(url, this.utilsService.getJsonHeader())
        .pipe(
            retry(1)
        );
    }


    /*
        @function addStudent
        @param student: Student
        @return Observable<Student>
        @desc: add a student
    */
    addStudent(student: Student): Observable<Student> {
        const studentData = this.parseStudent(student);
        let url = `${this.utilsService.getEndPoint().apiUrl}/student`;
        return this.http.post<Student>(url, studentData, this.utilsService.getJsonHeader())
        .pipe(
            retry(1)
        );
      }

    /*
        @function updateStudent
        @param student: Student
        @return Observable<Student>
        @desc: update a student
    */
    updateStudent(student: Student): Observable<Student> {
        const studentData = this.parseStudent(student);
        let url = `${this.utilsService.getEndPoint().apiUrl}/student/${student.id}`;
        return this.http.put<Student>(url, studentData, this.utilsService.getJsonHeader())
        .pipe(
            retry(1)
        );
      }

    /*
        @function getStudent
        @param id: number
        @return Observable<Student>
        @desc: get a student
    */
    getStudent(id: number): Observable<Student> {
        let url = `${this.utilsService.getEndPoint().apiUrl}/student/${id}`;
        return this.http.get<Student>(url, this.utilsService.getJsonHeader())
        .pipe(
            retry(1)
        );
    }

    /*
        @function deleteStudent
        @param id: number
        @return Observable<Student>
        @desc: delete a student
    */
    deleteStudent(id: number): Observable<Student> {
        let url = `${this.utilsService.getEndPoint().apiUrl}/student/${id}`;
        return this.http.delete<Student>(url, this.utilsService.getJsonHeader())
        .pipe(
            retry(1)
        );
    }

    /*
        @function parseStudent
        @param student: Student
        @return any
        @desc: parse a student to json
    */
    parseStudent(student: Student): any {
        return {
            "INE": student.INE,
            "name": student.user.name,
            "lastname": student.user.lastname,
            "password": student.user.password!,
            "username": student.user.username,
        }
    }


    /*
        @function getStudentsPerGroup
        @param idGroup: number
        @return Observable<Student[]>
        @desc: get all students for a group
    */
    getStudentsPerGroup(idGroup: number): Observable<Student[]> {
        let url = `${this.utilsService.getEndPoint().apiUrl}/students/groupe/${idGroup}`;
        return this.http.get<Student[]>(url, this.utilsService.getJsonHeader())
        .pipe(
            retry(1)
        );
    }
}
