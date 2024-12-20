import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  title = 'frontend';

  onHomeClick(): void {
    console.log('Button clicked!')
  }

  onAboutClick(): void {

  }

  onServicesClick(): void {

  }

  onContactClick(): void {

  }
}
