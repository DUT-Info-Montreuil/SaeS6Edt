import { Component } from '@angular/core';
import { Papa } from 'ngx-papaparse';
import { ToastrService } from 'ngx-toastr';
import { Observable } from 'rxjs';
import { Student } from 'src/app/_model/entity/student.model';
import { StudentService } from 'src/app/_service/student.service';
import { UserGroupService } from 'src/app/_service/user_group.service';

@Component({
  selector: 'app-csv-eleve-modal',
  templateUrl: './csv-eleve-modal.component.html',
  styleUrls: ['./csv-eleve-modal.component.scss']
})

export class CsvEleveModalComponent {
  constructor(
    private papa: Papa,
    private studentService: StudentService,
    private userGroupService: UserGroupService,
    private toastr: ToastrService
  ) {}

  onFileSelected(event: any) {
    const file: File = event.target.files[0];

    if (file) {
      this.parseCSV(file);
    }
  }

  parseCSV(file: File) {
    this.papa.parse(file, {
      complete: (result: any) => {
        // result.data contient les données du fichier CSV sous forme de tableau
        const students = result.data.slice(1); // Ignorer la première ligne (entêtes)
        // Traiter les étudiants ici et les envoyer au backend
        this.createStudents(students);
      }
    });
  }

  createStudent(eleve: Student): Observable<any> {
    return this.studentService.addStudent(eleve).pipe();
  }

  linkStudentToGroup(idStudent: number, idGroupe: number): Observable<any> {
    return this.userGroupService.addStudentToGroup(idStudent, idGroupe).pipe();
  }
  
  createStudents(students: any[]) {
    for (let index = 0; index < students.length - 1; index++) {
      const student = students[index];
      if (student[0]){
        let INE = parseInt(student[0], 10);
        let name = student[1];
        let lastname = student[2];
        let username = student[3];
        let password = student[4];
        let id_groupe = student[5];
        let eleve = new Student(0, INE, name, lastname, username, password);
        try {
            this.createStudent(eleve).subscribe(
              response => {
                this.linkStudentToGroup(response.id, id_groupe).subscribe();
              }
            );
          
        } catch (error) {
          this.toastr.error("Une erreur est survenue");
          console.log(eleve + " " + error);
        }
      }
    }
    this.userGroupService.notifyUserGroupRefresh();
  }
}
