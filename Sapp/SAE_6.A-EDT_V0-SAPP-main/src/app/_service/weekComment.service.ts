import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, retry } from 'rxjs';
import { WeekComment } from '../_model/entity/weekComment.model';
import { UtilsService } from './utils.service';


@Injectable({
    providedIn: 'root'
})
export class WeekCommentService {

    constructor(private http: HttpClient, private utilsService: UtilsService) { }


    /*
        @function getComments
        @return Observable<WeekComment[]>
        @desc: get all comments
    */
    getComments(): Observable<WeekComment[]> {
        let url = `${this.utilsService.getEndPoint().apiUrl}/week/comments`;
        return this.http.get<WeekComment[]>(url, this.utilsService.getJsonHeader())
        .pipe(
            retry(1)
        );
    }

    /*
        @function addComment
        @param comment: WeekComment
        @return Observable<WeekComment>
        @desc: add a comment
    */
    addComment(comment: WeekComment): Observable<WeekComment> {
        let url = `${this.utilsService.getEndPoint().apiUrl}/week/comment`;
        return this.http.post<WeekComment>(url, comment, this.utilsService.getJsonHeader())
        .pipe(
            retry(1)
        );
    }

    /*
        @function updateComment
        @param comment: WeekComment
        @return Observable<WeekComment>
        @desc: update a comment
    */
    updateComment(comment: WeekComment): Observable<WeekComment> {
        let url = `${this.utilsService.getEndPoint().apiUrl}/week/comment/${comment.id}`;
        return this.http.put<WeekComment>(url, comment, this.utilsService.getJsonHeader())
        .pipe(
            retry(1)
        );
    }

    /*
        @function getComment
        @param id: number
        @return Observable<WeekComment>
        @desc: get a comment
    */
    getComment(id: number): Observable<WeekComment> {
        let url = `${this.utilsService.getEndPoint().apiUrl}/week/comment/${id}`;
        return this.http.get<WeekComment>(url, this.utilsService.getJsonHeader())
        .pipe(
            retry(1)
        );
    }

    /*
        @function deleteComment
        @param id: string
        @return Observable<WeekComment>
        @desc: delete a comment
    */
    deleteComment(id: string): Observable<WeekComment> {
        let url = `${this.utilsService.getEndPoint().apiUrl}/week/comment/${id}`;
        return this.http.delete<WeekComment>(url, this.utilsService.getJsonHeader())
        .pipe(
            retry(1)
        );
    }
}
