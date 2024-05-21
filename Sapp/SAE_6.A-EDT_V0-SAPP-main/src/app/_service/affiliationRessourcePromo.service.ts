import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { UtilsService } from './utils.service';
import { Observable, retry } from 'rxjs';
import { Resource } from '../_model/entity/resource.model'
import { EdtManager } from '../_model/entity/edtManager.model';
import { Promotion } from '../_model/entity/promotion.model';

@Injectable({
    providedIn: 'root'
})
export class AffiliationRessourcePromo {

    constructor(private http: HttpClient, private utilsService: UtilsService) { }

    affiliateRessourceToPromo(idRessource: string, idPromo: number) : Observable<any>{
        let url = `${this.utilsService.getEndPoint().apiUrl}/affiliateRessourcePromo`;
        const requestBody = {
            id_ressource: idRessource,
            id_promo: idPromo
        };
        return this.http.post<any>(url, requestBody, this.utilsService.getJsonHeader())
        .pipe(
            retry(1)
        );
    }

    getRessourceByPromo(idPromo: number) : Observable<Resource[]>{
        let url = `${this.utilsService.getEndPoint().apiUrl}/getRessourcesByPromo/${idPromo}`;
        return this.http.get<Resource[]>(url, this.utilsService.getJsonHeader())
        .pipe(
            retry(1)
        );
    }

    getPromoByRessource(idRessource: string) : Observable<any>{
        let url = `${this.utilsService.getEndPoint().apiUrl}/getPromoByRessource/${idRessource}`;
        return this.http.get<any>(url, this.utilsService.getJsonHeader())
        .pipe(
            retry(1)
        );
    }

    deleteAffiliation(idRessource: string, idPromo: number) : Observable<any> {
        let url = `${this.utilsService.getEndPoint().apiUrl}/affiliateRessourcePromo/${idPromo}/${idRessource}`;
        return this.http.delete<any>(url, this.utilsService.getJsonHeader())
        .pipe(
            retry(1)
        );
    }
}