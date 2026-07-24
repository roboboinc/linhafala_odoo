odoo.define('linhafala_odoo.deficiente_form_save_button', function (require) {
    'use strict';

    const FormController = require('web.FormController');
    const core = require('web.core');
    const _t = core._t;

    FormController.include({
        saveRecord: function (params) {
            const self = this;

            // Only check for linhafala.deficiente model
            if (this.modelName !== 'linhafala.deficiente') {
                return this._super.apply(this, arguments);
            }

            // Validate before save
            const state = this.model.get(this.handle);
            if (state && state.data) {
                const data = state.data;
                const personId = data.person_id;

                // Check if person has are_you_disabled == 'Sim'
                if (personId && personId.data) {
                    const personData = personId.data;
                    const areYouDisabled = personData.are_you_disabled;

                    // Only enforce when are_you_disabled == 'Sim'
                    if (areYouDisabled === 'Sim') {
                        // Check if at least one option is selected
                        const hasSelection = !!(
                            data.vision_type ||
                            data.hearing_type ||
                            data.mobility_type ||
                            data.cognition_type ||
                            data.comunication_type ||
                            data.autonomous_care_type ||
                            data.what_disability_does_he_suffer
                        );

                        if (!hasSelection) {
                            this.displayNotification({
                                title: _t('Validation Error'),
                                message: _t('Selecione pelo menos uma opção em "Necessidades Especiais".'),
                                type: 'danger',
                                sticky: true,
                            });
                            return Promise.reject();
                        }
                    }
                }
            }

            return this._super.apply(this, arguments);
        }
    });
});
