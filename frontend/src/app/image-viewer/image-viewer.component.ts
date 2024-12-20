import { HttpClient } from '@angular/common/http';
import { Component, Injectable } from '@angular/core';

@Component({
  selector: 'app-image-viewer',
  imports: [],
  templateUrl: './image-viewer.component.html',
  styleUrl: './image-viewer.component.css'
})

@Injectable({ providedIn: 'root' })
export class ConfigService {
  constructor(private http: HttpClient) {
    
  }
}

export class ImageViewerComponent {
  onShowAllAvaliableBucketsClick(): void {
    // make a db call here from what you DIed with @Injectable
    
  }
}
