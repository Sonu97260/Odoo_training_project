/** @odoo-module **/

import { ListController } from "@web/views/list/list_controller";
import { listView } from "@web/views/list/list_view";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Component, onWillStart, useState } from "@odoo/owl";

/**
 * Custom List Controller for CRM Lead
 * Handles the Transfer Lead button visibility and action
 */
export class CrmLeadListController extends ListController {
    setup() {
        super.setup();
        
        // Initialize services
        this.actionService = useService("action");
        this.orm = useService("orm");
        this.notification = useService("notification");
        
        // Create reactive state for button visibility
        this.state = useState({
            showTransferButton: true
        });

        // Load button visibility setting when component mounts
        onWillStart(async () => {
            await this.loadButtonVisibility();
        });
    }

    /**
     * Load the button visibility setting from system parameters
     * This is called when the view is loaded
     */
    async loadButtonVisibility() {
        try {
            const result = await this.orm.call(
                "ir.config_parameter",
                "get_param",
                ["crm_leadgeneration.show_lead_transfer_button", "True"]
            );
            
            // Convert string result to boolean
            this.state.showTransferButton = result === "True";
            
            console.log("Transfer Button Visibility Loaded:", this.state.showTransferButton);
        } catch (error) {
            console.error("Error loading button visibility setting:", error);
            // Default to true if there's an error
            this.state.showTransferButton = true;
        }
    }

    /**
     * Handler for Transfer Lead button click
     * Opens the transfer wizard with selected leads
     */
    async onTransferLeadClick() {
        // Get selected record IDs
        const selectedRecords = await this.getSelectedResIds();
        
        // Validate selection
        if (!selectedRecords || selectedRecords.length === 0) {
            this.notification.add(
                "Please select at least one lead to transfer.",
                {
                    type: "warning",
                    title: "No Lead Selected",
                }
            );
            return;
        }

        console.log("Opening transfer wizard for leads:", selectedRecords);

        // Open the transfer wizard
        await this.actionService.doAction({
            type: "ir.actions.act_window",
            name: "Transfer Leads",
            res_model: "crm.lead.transfer.wizard",
            view_mode: "form",
            views: [[false, "form"]],
            target: "new",
            context: { 
                active_ids: selectedRecords,
                active_model: "crm.lead",
                default_lead_ids: selectedRecords,
            },
        });
    }
}

// Register the custom list view
export const customLeadListView = {
    ...listView,
    Controller: CrmLeadListController,
};

registry.category("views").add("crm_lead_list_context", customLeadListView);
