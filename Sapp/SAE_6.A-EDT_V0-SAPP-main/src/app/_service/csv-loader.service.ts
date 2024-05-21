import { Injectable } from '@angular/core';
import { Teacher } from '../_model/entity/teacher.model';
import { Papa } from 'ngx-papaparse';
import { Room } from '../_model/entity/room.model';
import { TeacherService } from './teacher.service';
import { RoomService } from './room.service';

@Injectable({
  providedIn: 'root'
})
export class CsvLoaderService {

  constructor(private parser: Papa, private teacherService: TeacherService, private roomService: RoomService) {}

  parseCSV(file: File): Promise<any> {
    return new Promise((resolve, reject) => {
      this.parser.parse(file, {
        complete: (result: any) => {
          const results = result.data.slice(1); // Ignore the first line (headers)
          resolve(results);
        },
        error: (error: any) => {
          reject(error);
        }
      });
    });
  }

  loadTeacherCSV(file: File) {
    this.parseCSV(file).then((result: any) => {
      this.teacherService.addTeacherCSV(result).subscribe();
    });
  }

  loadRoomCSV(file: File) {
    this.parseCSV(file).then((result: any) => {
      this.roomService.addSalleCSV(result).subscribe();
    });
  }

  onClick(event: any) {
    const file: File = event.target.files[0];

    if (file) {
      this.parseCSV(file);
    }
  }
}
