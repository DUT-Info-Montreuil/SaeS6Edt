import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, Subject, retry } from 'rxjs';
import { Resource } from '../_model/entity/resource.model';
import { UtilsService } from './utils.service';

@Injectable({
    providedIn: 'root'
})
export class ResourceService {

    constructor(private http: HttpClient, private utilsService: UtilsService) { }

    private ressourceRefreshSource = new Subject<void>();
    ressourceRefresh$ = this.ressourceRefreshSource.asObservable();


    /*
        @function notifyRessourceRefresh
        @return void
        @desc: notify all subscribers that a resource has been updated
    */
    notifyRessourceRefresh() {
        this.ressourceRefreshSource.next();
    }



    /*
        @function getResources
        @return Observable<Resource[]>
        @desc: get all resources
    */
    getResources(): Observable<Resource[]> {
        let url = `${this.utilsService.getEndPoint().apiUrl}/ressources`;
        return this.http.get<Resource[]>(url, this.utilsService.getJsonHeader())
        .pipe(
            retry(1)
        );
      }

    /*
        @function addResource
        @param resource: Resource
        @return Observable<Resource>
        @desc: add a resource
    */
    addResource(resource: Resource): Observable<Resource> {
        let url = `${this.utilsService.getEndPoint().apiUrl}/ressource`;
        return this.http.post<Resource>(url, resource, this.utilsService.getJsonHeader())
        .pipe(
            retry(1)
        );
      }

    /*
        @function updateResource
        @param resource: Resource
        @return Observable<Resource>
        @desc: update a resource
    */
    updateResource(resource: Resource): Observable<Resource> {
        let url = `${this.utilsService.getEndPoint().apiUrl}/ressource/${resource.initial}`;
        return this.http.put<Resource>(url, resource, this.utilsService.getJsonHeader())
        .pipe(
            retry(1)
        );
      }


    /*
        @function deleteResource
        @param resource: Resource
        @return Observable<Resource>
        @desc: delete a resource
    */
    deleteResource(resource: Resource): Observable<Resource> {
        let url = `${this.utilsService.getEndPoint().apiUrl}/ressource/${resource.initial}`;
        return this.http.delete<Resource>(url, this.utilsService.getJsonHeader())
        .pipe(
            retry(1)
        );
    }

    /*
        @function getResource
        @param id: number
        @return Observable<Resource>
        @desc: get a resource
    */
    
    getResource(id: number): Observable<Resource> {
        let url = `${this.utilsService.getEndPoint().apiUrl}/ressource/${id}`;
        return this.http.get<Resource>(url, this.utilsService.getJsonHeader())
        .pipe(
            retry(1)
        );
    }
}
