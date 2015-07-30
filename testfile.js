import React from 'react'

import ContentMain from './ContentMain'
import ContentSide from './ContentSide'
import ModalCreateMCQuestion from './CourseContent/ModalCreateMCQuestion'
import ModalConfirmation from './modules/ModalConfirmation.js'

var CourseBody = React.createClass({

    mixins: [React.addons.PureRenderMixin],

    propTypes: {
        ModuleItemStore: React.PropTypes.object.isRequired,
        ContentTreeStore: React.PropTypes.object.isRequired,
        CurrentCourseStore: React.PropTypes.object.isRequired
    },

    render: function () {
        let contentSide = false
        if (this.props.ContentTreeStore.get('hasContent')) {
            contentSide = (
                <ContentSide
                    ModuleItemStore={this.props.ModuleItemStore}
                    ContentTreeStore={this.props.ContentTreeStore}
                    CurrentCourseStore={this.props.CurrentCourseStore}
                />
            )
        }

        return (
            <div className="course_body">
                <ContentMain
                    ModuleItemStore={this.props.ModuleItemStore}
                    ContentTreeStore={this.props.ContentTreeStore}
                    CurrentCourseStore={this.props.CurrentCourseStore}
                />
                {contentSide}
                <ModalCreateMCQuestion/>
                <ModalConfirmation/>
            </div>
        )
    }
})

export default CourseBody
