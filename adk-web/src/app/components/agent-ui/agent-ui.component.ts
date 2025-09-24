import { Component, EventEmitter, OnInit, Output } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
	selector: 'app-agent-ui',
	templateUrl: './agent-ui.component.html',
	styleUrls: ['./agent-ui.component.scss'],
	imports: [CommonModule, FormsModule]
})
export class AgentUiComponent implements OnInit {

	@Output() weightsChange = new EventEmitter<any>();

	agents: string[] = [];
	selectedAgent: string = '';
	userQuery: string = '';
	weights: any = {
		market_potential: 25,
		finance_performance: 25,
		team_and_execution: 25,
		scalability_and_technology: 25
	};
	weightKeys = ['market_potential', 'finance_performance', 'team_and_execution', 'scalability_and_technology'];
	keyLabels: any = {
		market_potential: 'Market Potential',
		finance_performance: 'Finance Performance',
		team_and_execution: 'Team & Execution',
		scalability_and_technology: 'Scalability & Technology'
	};
	agentResponse: any = null;

	constructor(private http: HttpClient) { }

	ngOnInit() {
		this.http.get<string[]>('http://127.0.0.1:8080/list-apps?relative_path=./').subscribe(data => {
			this.agents = data;
			if (this.agents.length) this.selectedAgent = this.agents[0];
		});
	}

	onWeightChange() {
		this.weightsChange.emit({ ...this.weights });
	}
}