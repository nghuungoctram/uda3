import { Component, OnInit, Input } from '@angular/core';
import { Drink, DrinksService } from 'src/app/services/drinks.service';
import { ModalController } from '@ionic/angular';
import { AuthService } from 'src/app/services/auth.service';

@Component({
  selector: 'app-drink-form',
  templateUrl: './drink-form.component.html',
  styleUrls: ['./drink-form.component.scss'],
})
export class DrinkFormComponent implements OnInit {
  @Input() drink: Drink;
  @Input() isCreated: boolean;

  constructor(
    public auth: AuthService,
    private modalController: ModalController,
    private drinkService: DrinksService
  ) { }

  ngOnInit() {
    if (this.isCreated) {
      this.drink = {
        id: -1,
        title: '',
        recipe: []
      };
      this.addMoreKindOfDrink();
    }
  }

  trackById(idx: number): any {
    return idx;
  }

  removeKindOfDrink(idx: number) {
    this.drink.recipe.splice(idx, 1);
  }

  saveEvent() {
    this.drinkService.drinkSaved(this.drink);
    this.closePopup();
  }

  addMoreKindOfDrink(idx: number = 0) {
    this.drink.recipe.splice(idx + 1, 0, { name: '', color: '#F98C60', parts: 1 });
  }

  deleteClicked() {
    this.drinkService.deleteDrink(this.drink);
    this.closePopup();
  }

  closePopup() {
    this.modalController.dismiss();
  }
}
