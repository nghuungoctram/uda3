import { Injectable } from '@angular/core';
import { JwtHelperService } from '@auth0/angular-jwt';
import { environment } from '../../environments/environment';

const JWTS_LOCAL_KEY = 'JWTS_LOCAL_KEY';
const JWTS_ACTIVE_INDEX_KEY = 'JWTS_ACTIVE_INDEX_KEY';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  url = environment.auth0.url;
  audience = environment.auth0.audience;
  clientId = environment.auth0.clientId;
  callbackURL = environment.auth0.callbackURL;
  token: string;
  payload: any;

  constructor() { }

  loginPath(callbackPath = '') {
    let path = 'https://';
    path += this.url + '/authorize?';
    path += 'audience=' + this.audience + '&';
    path += 'response_type=token&';
    path += 'client_id=' + this.clientId + '&';
    path += 'redirect_uri=' + this.callbackURL + callbackPath;
    return path;
  }

  isPermissionAccepted(permission: string) {
    return (this.payload && this.payload.permissions && this.payload.permissions.length && this.payload.permissions.indexOf(permission) >= 0) ? true : false;
  }

  setJWT() {
    localStorage.setItem(JWTS_LOCAL_KEY, this.token);
    if (this.token) {
      this.decodeJWT(this.token);
    }
  }

  getJWT() {
    this.token = localStorage.getItem(JWTS_LOCAL_KEY) || null;
    if (this.token) {
      this.decodeJWT(this.token);
    }
  }

  checkValidToken() {
    const fragment = window.location.hash.substr(1).split('&')[0].split('=');
    if (fragment[0] === 'access_token') {
      this.token = fragment[1];
      this.setJWT();
    }
  }

  logoutUser() {
    this.token = '';
    this.payload = null;
    this.setJWT();
  }

  activeJWT() {
    return this.token;
  }

  decodeJWT(token: string) {
    const jwtservice = new JwtHelperService();
    this.payload = jwtservice.decodeToken(token);
    return this.payload;
  }
}
