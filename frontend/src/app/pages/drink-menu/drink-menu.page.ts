import { Component, OnInit } from '@angular/core';
import { DrinksService, Drink } from '../../services/drinks.service';
import { ModalController } from '@ionic/angular';
import { DrinkFormComponent } from './drink-form/drink-form.component';
import { AuthService } from 'src/app/services/auth.service';

@Component({
  selector: 'app-drink-menu',
  templateUrl: './drink-menu.page.html',
  styleUrls: ['./drink-menu.page.scss'],
})
export class DrinkMenuPage implements OnInit {
  Object = Object;

  constructor(
    private auth: AuthService,
    public drinks: DrinksService,
    private modalController: ModalController
  ) { }

  ngOnInit() {
    this.drinks.getDrinks();
  }

  async formOpened(activedrink: Drink = null) {
    if (!this.auth.isPermissionAccepted('get:drinks-detail')) {
      return;
    }

    const getModel = await this.modalController.create({
      component: DrinkFormComponent,
      componentProps: { drink: activedrink, isCreated: !activedrink }
    });

    getModel.present();
  }
}
