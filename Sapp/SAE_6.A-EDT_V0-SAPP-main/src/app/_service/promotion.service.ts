import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, Subject, retry } from 'rxjs';
import { Promotion } from '../_model/entity/promotion.model';
import { UtilsService } from './utils.service';

@Injectable({
    providedIn: 'root'
})
export class PromotionService {


    constructor(private http: HttpClient, private utilsService: UtilsService) { }

    private promoRefreshSource = new Subject<void>();
    promoRefresh$ = this.promoRefreshSource.asObservable();


    /*
        @function notifyPromoRefresh
        @return void
        @desc: notify all subscribers that a promotion has been updated
    */
    notifyPromoRefresh() {
        this.promoRefreshSource.next();
    }


    /*
        @function getPromotions
        @return Observable<Promotion[]>
        @desc: get all promotions
    */
    getPromotions(): Observable<Promotion[]> {
        let url = `${this.utilsService.getEndPoint().apiUrl}/promotions`;
        return this.http.get<Promotion[]>(url, this.utilsService.getJsonHeader())
        .pipe(
            retry(1)
        );
      }

    /*
        @function addPromotion
        @param promotion: Promotion
        @return Observable<Promotion>
        @desc: add a promotion
    */
    addPromotion(promotion: Promotion): Observable<Promotion> {
        const promotionData = this.parsePromotion(promotion);
        let url = `${this.utilsService.getEndPoint().apiUrl}/promotion`;
        return this.http.post<Promotion>(url, promotionData, this.utilsService.getJsonHeader())
        .pipe(
            retry(1)
        );
      }

    /*
        @function updatePromotion
        @param promotion: Promotion
        @return Observable<Promotion>
        @desc: update a promotion
    */
    updatePromotion(promotion: Promotion): Observable<Promotion> {
        const promotionData = this.parsePromotion(promotion);

        let url = `${this.utilsService.getEndPoint().apiUrl}/promotion/${promotion.id}`;
        return this.http.put<Promotion>(url, promotionData, this.utilsService.getJsonHeader())
        .pipe(
            retry(1)
        );
      }


    /*
        @function getPromotion
        @param id: number
        @return Observable<Promotion>
        @desc: get a promotion
    */
    getPromotion(id: number): Observable<Promotion> {
        let url = `${this.utilsService.getEndPoint().apiUrl}/promotion/${id}`;
        return this.http.get<Promotion>(url, this.utilsService.getJsonHeader())
        .pipe(
            retry(1)
        );
    }

    desactiverPromo(promoId: number) {
        let url = `${this.utilsService.getEndPoint().apiUrl}/promotion/deactivate/${promoId}`;
        return this.http.put(url, this.utilsService.getJsonHeader())
        .pipe(
            retry(1)
        );
    }


    /*
        @function parsePromotion
        @param promotion: Promotion
        @return any
        @desc: parse a promotion to send to API
    */
    parsePromotion(promotion: Promotion): any {
        return {
            "niveau": promotion.niveau,
            "name": promotion.group.name,
            "year": promotion.year,
            "id_resp": promotion.id_resp
         };
    }
}
