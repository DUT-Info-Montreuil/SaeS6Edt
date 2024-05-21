import { Component } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { AuthService } from 'src/app/_security/auth.service';
import { StorageService } from 'src/app/_security/storage.service';

@Component({
  selector: 'app-logout',
  templateUrl: './logout.component.html',
  styleUrls: ['./logout.component.scss']
})

export class LogoutComponent {

  loginForm!: FormGroup
  loading: boolean = false;

  nbRdm: number = Math.floor(Math.random() * 7);
  imageName = "assets/images/Frame" + this.nbRdm + ".png"; 

  formLogin = new FormGroup({
    identifier: new FormControl("", Validators.required),
    password: new FormControl("", Validators.required)
  })

  constructor(
    private authService: AuthService
  ){}

  ngOnInit() {
    this.authService.logoutUser();
  }
}