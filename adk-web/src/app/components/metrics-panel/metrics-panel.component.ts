import { Component, EventEmitter, Output } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';

@Component({
  selector: 'app-metrics-panel',
  templateUrl: './metrics-panel.component.html',
  styleUrls: ['./metrics-panel.component.scss']
})
export class MetricsPanelComponent {
  metricsEnabled = false;
  metricsForm: FormGroup;

  @Output() metricsChanged = new EventEmitter<any>();

  constructor(private fb: FormBuilder) {
    this.metricsForm = this.fb.group({
      financial_data: [50],
      traction_signals: [50],
      market_opportunity: [50],
    });

    this.metricsForm.valueChanges.subscribe(value => {
      if (this.metricsEnabled) {
        this.metricsChanged.emit(value);
      }
    });
  }

  toggleMetrics(enabled: boolean) {
    this.metricsEnabled = enabled;
    if (this.metricsEnabled) {
      this.metricsChanged.emit(this.metricsForm.value);
    } else {
      this.metricsChanged.emit(null);
    }
  }

  formatLabel(value: number) {
    return `${value}%`;
  }
}
