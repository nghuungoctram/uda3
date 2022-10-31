import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { AuthService } from './auth.service';
import { environment } from 'src/environments/environment';

export interface Drink {
  id: number;
  title: string;
  recipe: Array<{
    name: string,
    color: string,
    parts: number
  }>;
}

@Injectable({
  providedIn: 'root'
})
export class DrinksService {
  url = environment.apiServerUrl;
  public items: { [key: number]: Drink } = {};

  constructor(private auth: AuthService, private http: HttpClient) { }

  getTokenHeaders() {
    const header = {
      headers: new HttpHeaders()
        .set('Authorization', `Bearer ${this.auth.activeJWT()}`)
    };
    return header;
  }

  getDrinks(drinks: Array<Drink>) {
    for (const drink of drinks) {
      this.items[drink.id] = drink;
    }
  }

  getDrinkDetail() {
    if (this.auth.isPermissionAccepted('get:drinks-detail')) {
      this.http.get(this.url + '/drinks-detail', this.getTokenHeaders())
        .subscribe((res: any) => {
          this.getDrinks(res.drinks);
        });
    } else {
      this.http.get(this.url + '/drinks', this.getTokenHeaders())
        .subscribe((res: any) => {
          this.getDrinks(res.drinks);
        });
    }
  }

  deleteDrink(drink: Drink) {
    delete this.items[drink.id];
    this.http.delete(this.url + '/drinks/' + drink.id, this.getTokenHeaders())
      .subscribe((res: any) => {
        console.log(res)
      });
  }

  drinkSaved(drink: Drink) {
    if (drink && drink.id && drink.id >= 0) {
      this.http.patch(this.url + '/drinks/' + drink.id, drink, this.getTokenHeaders())
        .subscribe((res: any) => {
          if (res.success) {
            this.getDrinks(res.drinks);
          }
        });
    } else {
      this.http.post(this.url + '/drinks', drink, this.getTokenHeaders())
        .subscribe((res: any) => {
          if (res.success) {
            this.getDrinks(res.drinks);
          }
        });
    }
  }
}
