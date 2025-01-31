import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LoginComponent } from './login/login.component';
import { QueryComponent } from './query/query.component';
import { SignupComponent } from './signup/signup.component';  // Import SignUpComponent
import { ResetPasswordComponent } from './reset-password/reset-password.component';  // Import ResetPasswordComponent

const routes: Routes = [
  { path: 'login', component: LoginComponent },
  { path: 'query', component: QueryComponent },
  { path: 'signup', component: SignupComponent },
  { path: 'reset-password/:uid/:token', component: ResetPasswordComponent },
  { path: '', redirectTo: '/login', pathMatch: 'full' },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}
