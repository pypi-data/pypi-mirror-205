import jsPsychImageKeyboardResponse from '@jspsych/plugin-image-keyboard-response'
import 'jspsych/css/jspsych.css'

const main = async (id, condition) => {

    const trials = [
        {
            timeline: [{
                type: jsPsychImageKeyboardResponse, stimulus: () => {
                    let src = "test.png";
                    return src
                }, choices: () => {
                    let choices = [' '];
                    return choices
                }, on_finish: (data) => {
                    data["bean_type"] = 'jsPsychImageKeyboardResponse';
                    let src = "test.png";
                    data["bean_src"] = src;
                    let choices = [' '];
                    data["bean_choices"] = choices;
                    let correct_key = "";
                    data["bean_correct_key"] = correct_key;
                    data["bean_correct"] = correct_key == data["response"]
                }
            }], timeline_variables: condition[0]
        }]
    return await condition
}
export default main
