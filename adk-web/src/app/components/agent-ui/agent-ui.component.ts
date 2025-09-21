import { Component, EventEmitter, OnInit, Output } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-agent-ui',
  templateUrl: './agent-ui.component.html',
  styleUrls: ['./agent-ui.component.scss'],
  imports:[CommonModule,FormsModule]
})
export class AgentUiComponent implements OnInit {

  @Output() weightsChange = new EventEmitter<any>();

  agents: string[] = [];
  selectedAgent: string = '';
  userQuery: string = '';
  weights: any = {
    financial_data: 25,
    traction_signals: 25,
    market_opportunity: 25,
    team_quality: 25
  };
  weightKeys = ['financial_data', 'traction_signals', 'market_opportunity', 'team_quality'];
  keyLabels: any = {
    financial_data: 'Financial Data',
    traction_signals: 'Traction Signals',
    market_opportunity: 'Market Opportunity',
    team_quality: 'Team Quality'
  };
  agentResponse: any = null;

  constructor(private http: HttpClient) {}

  ngOnInit() {
    this.http.get<string[]>('http://127.0.0.1:8001/api/agents').subscribe(data => {
      this.agents = data;
      if (this.agents.length) this.selectedAgent = this.agents[0];
    });
  }

  onWeightChange() {
    this.weightsChange.emit({ ...this.weights });
  }
}