import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { format } from 'date-fns';
import { Observable, retry } from 'rxjs';
import { Course } from '../_model/entity/course.model';
import { UtilsService } from './utils.service';


@Injectable({
    providedIn: 'root'
})
export class CourseService {

    constructor(private http: HttpClient, private utilsService: UtilsService) { }


    /*
        @function getCourses
        @param args: array of filters
        @return Observable<Course[]>
        @desc: get courses from API with filters
    */
    getCourses(args: any[]= []): Observable<Course[]> {


        let params: String[] = []

        args.forEach(arg => {
            const key = Object.keys(arg)[0];
            params.push(`${key}=${arg[key]}`);
        });
        


        let url = `${this.utilsService.getEndPoint().apiUrl}/courses`;

        if (params.length > 0) {
            url += `?${params.join('&')}`;
        }


        

        return this.http.get<Course[]>(url, this.utilsService.getJsonHeader())
        .pipe(
            retry(1)
        );
      }

      /*
        @function getCoursesWithDate
        @param date_min: string
        @param date_max: string
        @return Observable<Course[]>
        @desc: get courses from API with filters
        */


      getCoursesWithDate(date_min:string, date_max:string): Observable<Course[]> {
        let url = `${this.utilsService.getEndPoint().apiUrl}/courses?date_min=${date_min}&date_max=${date_max}`;
        return this.http.get<Course[]>(url, this.utilsService.getJsonHeader())
        .pipe(
            retry(1)
        );
      }

     /*
        @function addCourse
        @param course: Course
        @return Observable<Course>
        @desc: add a course to API
    */
    addCourse(course: Course): Observable<Course> {
        const courseData = this.parseCourse(course);

        let url = `${this.utilsService.getEndPoint().apiUrl}/course`;
        return this.http.post<Course>(url, courseData, this.utilsService.getJsonHeader())
        .pipe(
            retry(1)
        );
      }

    /*
        @function updateCourse
        @param course: Course
        @return Observable<Course>
        @desc: update a course to API
    */
    updateCourse(course: Course): Observable<Course> {
        const courseData = this.parseCourse(course);

        let url = `${this.utilsService.getEndPoint().apiUrl}/course/${course.id}`;
        return this.http.put<Course>(url, courseData, this.utilsService.getJsonHeader())
        .pipe(
            retry(1)
        );
    }

      /*
        @function getCourse
        @param id: number
        @return Observable<Course>
        @desc: get a course from API
    */
    getCourse(id: number): Observable<Course> {
        let url = `${this.utilsService.getEndPoint().apiUrl}/course/${id}`;
        return this.http.get<Course>(url, this.utilsService.getJsonHeader())
        .pipe(
            retry(1)
        );
    }


    /*
        @function parseCourse
        @param course: Course
        @return any
        @desc: parse a course to send to API
    */
    parseCourse(course: Course): any {
        let isInDraft: boolean = false;
        if (course.start_time.getDay() == 6){
            isInDraft = true;
        }

        let courseParsed = {
            id: course.id,
            start_time: format(course.start_time, 'yyyy-MM-dd HH:mm:ss'),
            end_time: format(course.end_time, 'yyyy-MM-dd HH:mm:ss'),
            id_enseignant: course.id_enseignant,
            initial_ressource: course.initial_ressource,
            id_group: course.id_group,
            name_salle: course.name_salle,
            appelEffectue: course.appelEffectue,
            is_published: course.is_published,
            evaluation: course.evaluation,
            isInDraft: isInDraft
        }
        return courseParsed;
    }


    /*
        @function getCourse
        @desc: publish all course from API
    */
    publishCourses(){
        let url = `${this.utilsService.getEndPoint().apiUrl}/courses/publish`;
        return this.http.put(url, {}, this.utilsService.getJsonHeader())
        .pipe(
            retry(1)
        );
    }

    /*
        @function getCourse
        @desc: cancel publish for all course from API
    */
    cancelCourses(){
        let url = `${this.utilsService.getEndPoint().apiUrl}/courses/cancel`;
        return this.http.delete(url, this.utilsService.getJsonHeader())
        .pipe(
            retry(1)
        );
    }

    /*
        @function deleteCourse
        @param course: Course
        @return Observable<Course>
        @desc: delete a course from API
    */
    deleteCourse(course: Course): Observable<Course> {
        let url = `${this.utilsService.getEndPoint().apiUrl}/course/${course.id}`;
        return this.http.delete<Course>(url, this.utilsService.getJsonHeader())
        .pipe(
            retry(1)
        );
    }

    /*
        @function pasteCourse
        @param start_time: string
        @param end_time: string
        @param id_group: number
        @param start_time_attempt: string
        @param sat_date: string
        @param sun_date: string
        @return Observable<Course>
        @desc: paste a course from API
    */

    pasteCourse(start_time: string, end_time: string, id_group: number, start_time_attempt: string, sat_date: string, sun_date: string): Observable<Course> {
        let url = `${this.utilsService.getEndPoint().apiUrl}/courses/paste`;
        
        const body = {
            start_time: start_time,
            end_time: end_time,
            id_group: id_group,
            start_time_attempt: start_time_attempt,
            sat_date: sat_date,
            sun_date: sun_date
        };
    
        return this.http.post<Course>(url, body, this.utilsService.getJsonHeader())
            .pipe(
                retry(1)
            );
    }

    /*
        @function duplicate
        @param courseId: number
        @param groupsToDuplicateTo: number[]
        @return Observable<Course>
        @desc: duplicate a course from API
    */

    duplicate(courseId: number, groupsToDuplicateTo: number[]) {
        let url = `${this.utilsService.getEndPoint().apiUrl}/courses/duplicate`;

        const body = {
            courseId: courseId,
            groupsToDuplicateTo: groupsToDuplicateTo
        };
        
        return this.http.post<Course>(url, body, this.utilsService.getJsonHeader())
        .pipe(
            retry(1)
        );
    }

    /* 
        @function getStatsTeacher
        @param id_teacher: number
        @return Observable<Course[]>
        @desc: get stats for a teacher from API
    */

    getStatsTeacher(id_teacher: number): Observable<Course[]> {
        let url = `${this.utilsService.getEndPoint().apiUrl}/courses/stats/${id_teacher}`;

        return this.http.get<any[]>(url, this.utilsService.getJsonHeader())
        .pipe(
            retry(1)
        );
    }
}
