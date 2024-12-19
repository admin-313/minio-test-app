import { Routes } from '@angular/router';
import { ImageGetterComponent } from './image-getter/image-getter.component';
import { ImageViewerComponent } from './image-viewer/image-viewer.component';
import { PageNotFoundComponent } from './page-not-found/page-not-found.component';

export const routes: Routes = [
    { path: 'getimage', component: ImageGetterComponent },
    { path: 'viewimage', component: ImageViewerComponent },
    { path: '**', component: PageNotFoundComponent },
];
