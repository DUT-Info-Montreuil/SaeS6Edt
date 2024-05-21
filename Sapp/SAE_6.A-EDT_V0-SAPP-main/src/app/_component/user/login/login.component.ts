import { Component } from '@angular/core';
import { FormControl, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ToastrService } from 'ngx-toastr';
import { Router } from '@angular/router';
import { AuthService } from 'src/app/_security/auth.service';
import { AuthResponse } from 'src/app/_model/fonctional/auth-response.model';
import { StorageService } from 'src/app/_security/storage.service';

@Component({
  selector: 'app-acceuil',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})

export class LoginComponent {

  password: String;
  
  loginForm!: FormGroup;
  loading: boolean = false;

  nbRdm: number = Math.floor(Math.random() * 7);
  imageName = "assets/images/Frame" + this.nbRdm + ".png"; 

  formLogin = new FormGroup({
    identifier: new FormControl("", Validators.required),
    password: new FormControl("", Validators.required)
  })

  constructor(private toastr: ToastrService,
    private router: Router,
    private formBuilder: FormBuilder,
    private authService: AuthService,
    private storageService: StorageService) 
  { }

  ngOnInit() {
    this.password = 'password';
    this.loading = true;
    this.loginForm = this.formBuilder.group({
      username: ['', [
        Validators.required,
      ]],
      password: ['', [
        Validators.required, 
      ]]
    })
    this.loading = false;
  }

  onSubmit() {
    if (this.loginForm.invalid) {
      this.toastr.warning('veuillez rensegner un identifiant et/ou un mot de passe');
      return;
    }    
    const { username, password } = this.loginForm.value;
    this.authService.login(username.trim().toLowerCase(), password).subscribe({
      next: (data: AuthResponse) => {
        this.storageService.saveResponse(data);
        this.router.navigate(['/edt']);
        this.toastr.success('vous etes bien connecté');
      },
      error: err => {
        this.toastr.error('identifiant et/ou un mot de passe incorect(s)');
      }
    });
  }

  onClick(){
    if (this.password === 'password') {
      this.password = 'text';
    } else {
      this.password = 'password';
    }
  }
}