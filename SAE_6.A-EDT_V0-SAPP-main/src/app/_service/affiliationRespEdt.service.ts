import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { UtilsService } from './utils.service';
import { Observable, retry } from 'rxjs';
import { EdtManager } from '../_model/entity/edtManager.model';
import { Promotion } from '../_model/entity/promotion.model';

@Injectable({
    providedIn: 'root'
})
export class AffiliationRespEdtService {

    constructor(private http: HttpClient, private utilsService: UtilsService) { }


    /*
        @function affiliateRespEdtToPromo
        @param idResp: number
        @param idPromo: number
        @return Observable<any>
        @desc: get all affiliate a respEdt with promotion
    */

    affiliateRespEdtToPromo(idResp : number, idPromo : number) : Observable<any>{
        let url = `${this.utilsService.getEndPoint().apiUrl}/affiliateRespEdt`;

        const requestBody = {
            id_resp: idResp,
            id_promo: idPromo
        };

        return this.http.post<any>(url, requestBody, this.utilsService.getJsonHeader())
        .pipe(
            retry(1)
        );
    }

    /*
        @function getPromosForRespEdt
        @param idResp: number
        @return Observable<Promotion[]>
        @desc: get all promotions for a respEdt
    */

    getPromosForRespEdt(idResp : number) : Observable<Promotion[]>{
        let url = `${this.utilsService.getEndPoint().apiUrl}/affiliateRespEdt/getPromosByResp/${idResp}`;
        return this.http.get<Promotion[]>(url, this.utilsService.getJsonHeader())
        .pipe(
            retry(1)
        );
    }


    /*
        @function getRespEdtByPromo
        @param idPromo: number
        @return Observable<EdtManager[]>
        @desc: get all respEdt for a promotion
    */
    getRespEdtByPromo(idPromo : number) : Observable<EdtManager[]>{
        let url = `${this.utilsService.getEndPoint().apiUrl}/affiliateRespEdt/getRespByPromo/${idPromo}`;
        return this.http.get<EdtManager[]>(url, this.utilsService.getJsonHeader())
        .pipe(
        );
    }


    /*
        @function deleteAffiliation
        @param idResp: number
        @return Observable<any>
        @desc: delete affiliation between a respEdt and a promotion
    */  
    deleteAffiliation(idResp : number) : Observable<any>{
        let url = `${this.utilsService.getEndPoint().apiUrl}/affiliateRespEdt/delete/${idResp}`;
        return this.http.delete<any>(url, this.utilsService.getJsonHeader())
        .pipe(
            retry(1)
        );
    }

    /*
        @function deleteAffiliationPromoResp
        @param idResp: number
        @param idPromo: number
        @return Observable<any>
        @desc: delete affiliation between a respEdt and a promotion
    */

    deleteAffiliationPromoResp(idResp : number, idPromo: number) : Observable<any>{
        let url = `${this.utilsService.getEndPoint().apiUrl}/affiliateRespEdt/delete/${idResp}/${idPromo}`;
        return this.http.delete<any>(url, this.utilsService.getJsonHeader())
        .pipe(
            retry(1)
        );
    }
}