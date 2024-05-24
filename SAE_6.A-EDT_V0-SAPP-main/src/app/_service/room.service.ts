import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, Subject, retry } from 'rxjs';
import { Room } from '../_model/entity/room.model';
import { UtilsService } from './utils.service';


@Injectable({
    providedIn: 'root'
})
export class RoomService {

    constructor(private http: HttpClient, private utilsService: UtilsService) { }

    private salleRefreshSource = new Subject<void>();
    salleRefresh$ = this.salleRefreshSource.asObservable();


    /*
        @function notifySalleRefresh
        @return void
        @desc: notify all subscribers that a room has been updated
    */
    notifySalleRefresh() {
        this.salleRefreshSource.next();
    }



    /*
        @function getSalles
        @return Observable<Room[]>
        @desc: get all rooms
    */
    getSalles(): Observable<Room[]> {
        let url = `${this.utilsService.getEndPoint().apiUrl}/salles`;
        return this.http.get<Room[]>(url, this.utilsService.getJsonHeader())
        .pipe(
            retry(1)
        );
    }

    /*
        @function addSalle
        @param room: Room
        @return Observable<Room>
        @desc: add a room
    */
    addSalle(room: Room): Observable<Room> {
        let url = `${this.utilsService.getEndPoint().apiUrl}/salle`;
        return this.http.post<Room>(url, room, this.utilsService.getJsonHeader())
        .pipe(
            retry(1)
        );
    }

    addSalleCSV(csv: any): Observable<any> {
        let url = `${this.utilsService.getEndPoint().apiUrl}/salles/csv`;
        return this.http.post<any>(url, csv, this.utilsService.getJsonHeader())
        .pipe(
            retry(1)
        );
    }

    /*
        @function updateSalle
        @param room: Room
        @return Observable<Room>
        @desc: update a room
    */
    updateSalle(room: Room): Observable<Room> {
        let url = `${this.utilsService.getEndPoint().apiUrl}/salle/${room.nom}`;
        return this.http.put<Room>(url, room, this.utilsService.getJsonHeader())
        .pipe(
            retry(1)
        );
    }

    /*
        @function getSalle
        @param id: number
        @return Observable<Room>
        @desc: get a room
    */
    getSalle(id: number): Observable<Room> {
        let url = `${this.utilsService.getEndPoint().apiUrl}/salle/${id}`;
        return this.http.get<Room>(url, this.utilsService.getJsonHeader())
        .pipe(
            retry(1)
        );
    }

    /*
        @function deleteSalle
        @param name: string
        @return Observable<Room>
        @desc: delete a room
    */
    deleteSalle(name: string): Observable<Room> {
        let url = `${this.utilsService.getEndPoint().apiUrl}/salle/${name}`;
        return this.http.delete<Room>(url, this.utilsService.getJsonHeader())
        .pipe(
            retry(1)
        );
    }
}
