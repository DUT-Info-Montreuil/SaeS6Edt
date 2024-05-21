import { Component, Inject, OnInit } from '@angular/core';
import { MAT_DIALOG_DATA } from '@angular/material/dialog';
import { ToastrService } from 'ngx-toastr';
import { Observable, catchError, map } from 'rxjs';
import { AffiliationRespEdtService } from 'src/app/_service/affiliationRespEdt.service';
import { EdtManagerService } from 'src/app/_service/edtManager.service';
import { GroupService } from 'src/app/_service/group.service';
import { ResourceService } from 'src/app/_service/resource.service';
import { RoomService } from 'src/app/_service/room.service';
import { StudentService } from 'src/app/_service/student.service';
import { TeacherService } from 'src/app/_service/teacher.service';

@Component({
  selector: 'app-delete-modal',
  templateUrl: './delete-modal.component.html',
  styleUrls: ['./delete-modal.component.scss']
})

export class DeleteModalComponent implements OnInit{
  elementASupp: string;

  public formSelectionne: any = null;

  constructor(
    @Inject(MAT_DIALOG_DATA) public data: any,
    private teacherService: TeacherService,
    private roomService: RoomService,
    private ressourceService: ResourceService,
    private studentService: StudentService,
    private groupService: GroupService,
    private affiliationService: AffiliationRespEdtService,
    private responsableService: EdtManagerService,
    private toastr: ToastrService
  ){}

  ngOnInit(): void {
    this.formSelectionne = this.data.formSelectionne;
    this.setElementASupp();
  }

  setElementASupp(){
    switch (this.formSelectionne) {
      case "formSalle":
        this.elementASupp = this.data.element.nom;
        break;
      case "formProfesseur" || "formResponsable":
        this.elementASupp = this.data.element.staff.user.name + " " + this.data.element.staff.user.lastname;
        break;
      case "formRessource":
        this.elementASupp = this.data.element.initial;
        break;
      case "formEleve":
        this.elementASupp = this.data.element.user.name + " " + this.data.element.user.lastname;
        break;
      case "formGroupe":
        this.elementASupp = this.data.element.name;
        break;
      case "formPromo":
        this.elementASupp = ' cette affiliation';
        break;
    }
  }

  responsablesChanged() {
    this.responsableService.notifyRespRefresh();
  }

  groupesChanged(){
    this.groupService.notifyGroupRefresh();
  }

  studentsChanged(){
    this.studentService.notifyStudentRefresh();
  }

  sallesChanged() {
    this.roomService.notifySalleRefresh();
  }

  profsChanged(){
    this.teacherService.notifyProfRefresh();
  }

  ressourcesChanged(){
    this.ressourceService.notifyRessourceRefresh();
  }

  supprimerAffiliationRespEdt(): Observable<any> {
    return this.affiliationService.deleteAffiliation(this.data.element.id).pipe(
        map(response => {
          return response;
        }),
        catchError(error => {
          console.log(error);
          this.toastr.error("Erreur lors de la suppression de l'affiliation.");
          return error;
        })
    );
}

  supprimerResponsable(){
    this.supprimerAffiliationRespEdt().subscribe({
      next: response => {
        this.responsableService.deleteEdtManager(this.data.element.id).subscribe({
          next: response => {
            this.toastr.success("le responsable a bien été supprimé!");
            this.responsablesChanged();
          },
          error: error=> {
            this.toastr.error("Impossible de supprimer le résponsable tant qu'il est affecté à d'autres entité");
            console.log(error);
          }
        });
      }
    });
    this.elementASupp = "";
  }

  supprimerSalle(){
    this.roomService.deleteSalle(this.data.element.nom).subscribe({
      next: response => {
        this.toastr.success("la salle a bien été supprimée!");
        this.sallesChanged();
      },
      error: error=> {this.toastr.error("erreur");}
    });
    this.elementASupp = "";
  }

  supprimerProf(){
    this.teacherService.deleteTeacher(this.data.element.id).subscribe({
      next: response => {
        this.toastr.success("le professeur a bien été supprimé!");
        this.profsChanged();
      },
      error: error=> {this.toastr.error("erreur");}
    });
    this.elementASupp = "";
  }

  // code 200 mais ne supprime pas la ressource dans la liste
  supprimerRessource(){
    this.ressourceService.deleteResource(this.data.element).subscribe({
      next: response => {
        this.toastr.success("la ressource a bien été supprimée!");
        this.ressourcesChanged();
      },
      error: error=> {this.toastr.error("erreur");}
    });
    this.elementASupp = "";
  }

  supprimerEleve() {
    this.studentService.deleteStudent(this.data.element.id).subscribe({
      next: response => {
        this.toastr.success("l'eleve a bien été supprimé!");
        this.studentsChanged();
      },
      error: error=> {
        this.toastr.error("une erreur est survenue lors de la suppression");
        console.log(error);
      }
    });
    this.elementASupp = "";
  }

  supprimerGroupe(){
    this.groupService.deleteGroup(this.data.element.id).subscribe({
      next: response => {
        this.toastr.success("le groupe a bien été supprimé!");
        this.groupesChanged();
      },
      error: error=> {this.toastr.error("erreur");}
    });
    this.elementASupp = "";
  }

  supprimerAffiliationPromoResp(){
    this.affiliationService.deleteAffiliationPromoResp(this.data.element.id_resp, this.data.element.id_promo).subscribe({
      next: response => {
        this.toastr.success("l'affiliation a bien été supprimée!");
        location.reload();
      },
      error: error=> {this.toastr.error("erreur");}
    });
  }
}