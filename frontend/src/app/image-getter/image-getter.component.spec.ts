import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ImageGetterComponent } from './image-getter.component';

describe('ImageGetterComponent', () => {
  let component: ImageGetterComponent;
  let fixture: ComponentFixture<ImageGetterComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ImageGetterComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ImageGetterComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
