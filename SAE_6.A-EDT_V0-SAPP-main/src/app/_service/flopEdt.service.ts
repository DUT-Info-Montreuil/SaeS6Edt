import { HttpClient} from "@angular/common/http";
import {Injectable} from "@angular/core";
import {UtilsService} from "./utils.service";

@Injectable({
  providedIn: 'root'
})
export class FlopEdtService {

  constructor(private http: HttpClient, private utilsService: UtilsService) { }


  importFlopEdt(dept : string, week : number, year : number, work_copy : number) {
    let url = `${this.utilsService.getEndPoint().apiUrl}/flopEdt`;

    const body = {
      dept: dept,
      week: week,
      year: year,
      work_copy: work_copy
    };

    return this.http.post(url, body, this.utilsService.getJsonHeader());
  }
}
