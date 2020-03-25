odoo.define('base_import_one2many.import_action', function(require) {
    "use strict";

    var core = require('web.core');
    var Model = require('web.BasicModel');
    var DataImport = require('base_import.import');
    var Dialog = require('web.Dialog');

    DataImport.DataImport.include({

        init: function(parent, action) {
            this._super.apply(this, arguments);
            this._target = action.target;
            this.parent_field = action.params.parent_field || false;
            this.action_id = action.jsID;
            if (this.is_one2many_import()) {
                this.parentController = this.action_manager.getCurrentController();
            }
        },

        is_one2many_import: function() {
            return this._target == 'new' && this.parent_field;
        },

        exit: function() {
            if (!this.is_one2many_import()) {
                return this._super.apply(this, arguments);
            }
            if (this.action_manager.currentDialogController) {
                this.action_manager.currentDialogController.dialog.close();
            }
        },

        import_options: function() {
            var options = this._super.apply(this, arguments);
            if (options && this.is_one2many_import()) {
                var controller = this.getController();
                var model = controller.model;
                var parent = model.get(controller.handle);
                _.extend(options, {
                    import_one2many: this.is_one2many_import(),
                    parent_field: parent.fields[this.parent_field].relation_field + '.id',
                    parent_id: parent.data['id'],
                });
            }
            return options;
        },

        getController: function() {
            return this.action_manager.getCurrentController().widget;
        },

        renderButtons: function(footer) {
            this._super.apply(this, arguments);
            if (footer && this.is_one2many_import()) {
                var controller = this.action_manager.currentDialogController;
                if (controller && controller.dialog) {
                    controller.dialog.$el.css('height', '450px');
                    footer.append(this.$buttons);
                }
            }
        },

    });

});
