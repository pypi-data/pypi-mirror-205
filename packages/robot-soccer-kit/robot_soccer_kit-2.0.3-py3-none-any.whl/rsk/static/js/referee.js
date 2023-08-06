function referee_initialize(backend)
{
    let displayed_toast_nb = 0 ;

    let event_neutral_tpl = '';
    $.get('/static/referee_event_neutral.html', function(data) {
        event_neutral_tpl = data;
    });
    let event_team_tpl = ''
    $.get('/static/referee_event_team.html', function(data) {
        event_team_tpl = data;
    });

    backend.constants(function(constants) {
        setInterval(function() {
            backend.get_game_state(function(game_state) {

                let first_team = constants["team_colors"][0]
                let second_team = constants["team_colors"][1]

                // Team names
                $(".first-team-name").text(game_state["teams"][first_team]["name"] || constants["team_colors"][0]);
                $(".second-team-name").text(game_state["teams"][second_team]["name"] || constants["team_colors"][1]);

                // Robots State
                for (let team in game_state["teams"]) {
                    let team_data = game_state["teams"][team]
                    for (let number in team_data["robots"]) {
                        let robot = team_data["robots"][number]

                        let remaining = robot["penalized_remaining"]
                        let penalty_reason = robot["penalized_reason"]

                        let bar = $('.robot-penalty[rel='+team+number+'] .progress-bar')
                        if (remaining !== null) {
                            let pct = Math.min(100, remaining * 100. / constants.default_penalty);
                            bar.attr("style","width:"+pct+"%");
                            bar.html("<b>"+remaining+" s<b>");
                        } else {
                            bar.attr("style","width:0%");
                            bar.text('')
                        }


                        let reasons = robot["preemption_reasons"]
                        let div = $('.robot-penalty[rel='+team+number+'] .robot-state');
                        
                        if (reasons.length > 0) {
                            let reasons_string = reasons.join(',')
                            if (penalty_reason) {
                                reasons_string = "["+penalty_reason+"]"
                            }
                            div.html('<h6 class="text-danger">'+ reasons_string +'</h6>');

                        } 
                        else if (game_state["game_state_msg"] == "Game is running..."){
                            div.html('<h6>Robot is playing...</h6>');
                        }
                        else {
                            div.html('<h6>Robot is ready to play</h6>');
                        }
                    }
                }

                // Scores
                $("#GreenScore").html(game_state["teams"][first_team]["score"]);
                $("#BlueScore").html(game_state["teams"][second_team]["score"]);
                
                // Timer
                $('.TimerMinutes').html(formatTimer(game_state["timer"]))
                
                if(game_state["game_state_msg"] == "Game is running..."){
                    if (game_state["timer"] < 0) {
                        $(".TimerMinutes").addClass('text-danger');
                        $(".bg-body-grey").removeClass('bg-body-red');
                    } else if (game_state["timer"] < 10 && game_state["timer"]%2){
                        $(".bg-body-grey").addClass('bg-body-red');
                    } else {
                        $(".TimerMinutes").removeClass('text-danger');
                        $(".bg-body-grey").removeClass('bg-body-red');
                    }   
                } else {
                    $(".TimerMinutes").removeClass('text-danger');
                    $(".bg-body-grey").removeClass('bg-body-red');
                }


                // Game State
                $(".GameState").html(game_state["game_state_msg"]);

                if (!game_state["game_is_running"]){
                    $('.start-game').removeClass('d-none');
                    $('.pause-game-grp').addClass('d-none');
                    $('.resume-game-grp').addClass('d-none');

                    // Disable buttons when referee is not running
                    $("#MidTimeChange").prop("disabled", true);
                    $('.score-zone').each(function() {
                        $(this).find('.up-score').prop("disabled", true);
                        $(this).find('.down-score').prop("disabled", true);
                    });
                    $('.robot-penalty').each(function() {
                        $(this).find('.unpenalize').prop("disabled", true);
                        $(this).find('.penalize').prop("disabled", true);
                    });
                }

                else if (game_state["game_is_running"]){
                    $('.start-game').addClass('d-none');
                    $('.pause-game-grp').removeClass('d-none'); 

                    // Enable buttons when referee is running
                    $("#MidTimeChange").prop("disabled", false);
                    $('.score-zone').each(function() {
                        $(this).find('.up-score').prop("disabled", false);
                        $(this).find('.down-score').prop("disabled", false);
                    });
                    $('.robot-penalty').each(function() {
                        $(this).find('.unpenalize').prop("disabled", false);
                        $(this).find('.penalize').prop("disabled", false);
                    });

                    if (game_state["game_paused"]){
                        $('.resume-game-grp').removeClass('d-none');
                        $('.pause-game-grp').addClass('d-none');
                    } else  {
                        $('.pause-game-grp').removeClass('d-none');
                        $('.resume-game-grp').addClass('d-none');
                    }
                }
    
                //Disable Pause Button if a Goal is waiting for Validation
                if (game_state["game_state_msg"] == "Waiting for Goal Validation"){
                    $('.resume-game').prop("disabled", true);
                }
                else{
                    $('.resume-game').prop("disabled", false);
                }
                    


                // Referee History
                for (let history_entry of game_state["referee_history_sliced"]) {
                    [num, time, team, referee_event] = history_entry
                        $("#NoHistory").html('')

                        if (num >= displayed_toast_nb) {
                            let html = '';

                            let vars = {
                                'id': displayed_toast_nb,
                                'team': team,
                                'title': referee_event,
                                'timestamp': formatTimer(time),
                                'event': referee_event
                            };

                            if (team === 'neutral'){
                                html = event_neutral_tpl
                            } else {
                                html = event_team_tpl
                            }

                            for (let key in vars) {
                                html = html.replaceAll('{'+key+'}', vars[key])
                            }

                            $("#RefereeHistory").append(html);
                            $('#toast-'+displayed_toast_nb).toast('show');
                            $("#tchat").scrollTop($("#tchat")[0].scrollHeight);

                            displayed_toast_nb = displayed_toast_nb+1;

                        }
                }

                if (game_state["teams"][first_team]["x_positive"]){
                    $('.robot-penalize-tab').css("flex-direction", "row");
                }
                else {
                    $('.robot-penalize-tab').css("flex-direction", "row-reverse");
                }
            });

        }, 200);


    });

    $('.toast').toast('show');

    // Game Start&Stop
    $('.start-game').click(function() {
        backend.start_game();
        displayed_toast_nb = 0;
        $("#RefereeHistory").html('');
        $("#NoHistory").html('<h6 class="text-muted">No History</h6>');
    });

    $('.pause-game').click(function() {
        backend.pause_game();
    });

    $('.resume-game').click(function() {
        backend.resume_game();
    });

    $('.stop-game').click(function() {
        backend.stop_game();
    });

    
    // Half Time
    $('#MidTimeChange').click(function() {

        $("#RefereeHistory").append('<h5 class="text-muted m-3">Half Time</h5>');
        backend.start_half_time();
    });

    $('#ViewChange').click(function() {
          
    });

    $('#Y_ChangeCover').click(function() {
        $('.ChangeCover').addClass('d-none');
        $('.MidTimeIdentify').removeClass('d-none');
        $('.MidTimeIdentifyBefore').removeClass('d-none');
        backend.place_game('swap_covers');
    });

    $('#N_ChangeCover').click(function() {
        backend.place_game('gently_swap_side');
        backend.swap_team_sides();
        $('.ChangeCover').addClass('d-none');
        $('.SecondHalfTime').removeClass('d-none');
        setTimeout(function() {
            backend.place_game('standard');
        }, 5000);

    });

    $('#BtnMidTimeIdentify').click(function() {
        $('.MidTimeIdentifyBefore').addClass('d-none');
        $('.MidTimeIdentifyWait').removeClass('d-none');
        setTimeout(function() {
            $('.MidTimeIdentifyWait').addClass('d-none');
            $('#Next_MidTimeIdentify').removeClass('d-none');
            $('.MidTimeIdentifyDone').removeClass('d-none');
            $('.MidTimeIdentifyDone').removeClass('d-none');
            $('.MidTimeIdentifyWait').addClass('d-none');
            }, 4000);
    });

    $('#Next_MidTimeIdentify').click(function() {
        backend.swap_team_sides();
        $('#HalfTimePlaceStd').removeClass('d-none');
        $('#Next_MidTimeIdentify').addClass('d-none');
        $('.MidTimeIdentifyDone').addClass('d-none');
        $('.MidTimeIdentify').addClass('d-none');
        $('.MidTimeIdentifyBefore').addClass('d-none');
        $('.SecondHalfTime').removeClass('d-none');
        backend.place_game('standard');
    });

    $('#BtnSecondHalfTime').click(function() {
        setTimeout(function() {
        $('.ChangeCover').removeClass('d-none');
        $('.MidTimeIdentify').addClass('d-none');
        $('.SecondHalfTime').addClass('d-none');
        $('#HalfTimePlaceStd').addClass('d-none');
        }, 500);
        backend.start_second_half_time();
    });

    // Teams Names
    $( ".team-name" ).change(function() {
        backend.set_team_name($(this).attr('rel'), $(this).val())
    });

    // Scores 
    $('.score-zone').each(function() {
        let robot_id = $(this).attr('rel');

        $(this).find('.up-score').click(function() {
            backend.increment_score(robot_id, 1);
        });

        $(this).find('.down-score').click(function() {
            backend.increment_score(robot_id, -1);
        });
    });

    $("#RefereeHistory").on('click','.validate-goal', function() {
        backend.get_game_state(function(game_state) {
            last_referee_item = game_state["referee_history_sliced"].length-1
            id_last_referee_item = String(game_state["referee_history_sliced"][last_referee_item])
            nb = String(game_state["referee_history_sliced"].length-1)
            $("#toast-"+id_last_referee_item).find('.icon').removeClass('bi-circle-fill')
            $("#toast-"+id_last_referee_item).find('.icon').addClass('bi-check2-circle')
            $("#toast-"+id_last_referee_item).find('.toast-body').addClass('text-success')
            $("#toast-"+id_last_referee_item).find('.toast-body').html('<h5 class="m-0">Goal Validated</h5>')
        });
        backend.validate_goal(true)
    });

    $("#RefereeHistory").on('click','.cancel-goal', function() {
        backend.get_game_state(function(game_state) {
            last_referee_item = game_state["referee_history_sliced"].length-1
            id_last_referee_item = String(game_state["referee_history_sliced"][last_referee_item])
            $("#toast-"+id_last_referee_item).find('.icon').removeClass('bi-circle-fill')
            $("#toast-"+id_last_referee_item).find('.icon').addClass('bi-x-circle')
            $("#toast-"+id_last_referee_item).find('.toast-body').addClass('text-danger')
            $("#toast-"+id_last_referee_item).find('.toast-body').html('<h5 class="m-0">Goal Disallowed</h5>')
        });
        backend.validate_goal(false)
    });

    $('.reset-score').click(function() {
        backend.reset_score();
    });

    // Place Robots
    $('.strd-place').click(function() {
        backend.place_game('standard');
    });

    $('.dots-place').click(function() {
        backend.place_game('dots');
    });
    
    $('.side-place').click(function() {
        backend.place_game('side');
    });
    
    // Robots Penalties
    $('.robot-penalty').each(function() {
        let robot_id = $(this).attr('rel');

        $(this).find('.penalize').click(function() {
            backend.add_penalty(5, robot_id);
        });
        $(this).find('.unpenalize').click(function() {
            backend.cancel_penalty(robot_id);
        });
        $(this).find('.move').click(function() {
            
            $('.move').removeClass('btn-danger')
            if(selected_objet == robot_id){
                selected_objet = "ball";
            }else{
                $(this).addClass("btn-danger")
                selected_objet = robot_id;
            }
        });
    });

    simulated_view = false
    intervalId = 0
    let selected_objet = "ball"

    backend.constants(function(constants) {
        let carpet_size = [constants["carpet_length"], constants["carpet_width"]]

        var context = document.getElementsByTagName('canvas')[0].getContext('2d')
        ctx_width = context.canvas.width
        ctx_height = context.canvas.height
        robot_size = ctx_width/8
        var background = new Image()
        background.src = "static/imgs/field.svg"
        background.width = this.naturalWidth
        background.height = this.naturalHeight

        background.onload = function(){
            context.canvas.width = this.naturalWidth
            context.canvas.height = this.naturalHeight
            context.drawImage(background,0,0)
        }

        function meters_to_pixels_ratio() {
            return document.getElementById('back').offsetWidth / carpet_size[0]
        }

        function cam_to_sim(position, orientation) {
            let pos_sim = [0.0, 0.0, 0.0]
            pos = [position[0],position[1],orientation]
            ratio_w = document.getElementById('back').offsetWidth / carpet_size[0]
            ratio_h = document.getElementById('back').offsetHeight / carpet_size[1]
            pos_sim[0] = ((pos[0] + carpet_size[0]/2)* ratio_w)
            pos_sim[1] = ((-pos[1] + carpet_size[1]/2) * ratio_h) 
            pos_sim[2] = round(-pos[2]+Math.PI/2)
            return pos_sim  
        }
        function if_move(last_pos, position){
            min_translation = 1
            min_rotation = 0.05
            if (Math.abs(last_pos[0] - position[0]) > min_translation){
                    return true
            }else if (Math.abs(last_pos[1] - position[1]) >  min_translation){
                    return true
            }else if (Math.abs(last_pos[2] - position[2]) > min_rotation){
                    return true
            }
            return false
        }

        function draw_leds(color, context){
            for(i = -30; i<-30+120*3; i+= 120){
                angle =  i * Math.PI/180
                x = Math.round(Math.cos(angle)*constants["robot_radius"]*meters_to_pixels_ratio()*0.93)
                y = Math.round(Math.sin(angle)*constants["robot_radius"]*meters_to_pixels_ratio()*0.93)
                context.beginPath()
                gradient = context.createRadialGradient(x, y, 0, x, y, 70);
                gradient.addColorStop(0.05, "rgba("+color+",1)");
                gradient.addColorStop(0.1, "rgba("+color+",0.5)");
                gradient.addColorStop(0.25, "rgba("+color+",0)");
                context.fillStyle = gradient
                context.fillRect(x-25, y-25, 200, 200);
            }
        }

        function draw_circle(position, radius, color, canvas, clear=false, tickness=0){
            context = canvas.getContext('2d')
            if(clear) context.clearRect(0,0,canvas.width,canvas.height)
            context.beginPath()
            context.strokeStyle = color
            context.fillStyle = color
            context.arc(position[0], position[1], radius, 0, Math.PI*2);
            context.lineWidth = tickness    
            if(tickness==0) context.fill()
            else context.stroke()
        }

        function draw_ball(position){
            ball_canvas = document.getElementById("ball")
            ball = cam_to_sim(position)
            radius = constants["ball_radius"] * meters_to_pixels_ratio()
            draw_circle(ball, radius, "orange", ball_canvas, true)
        }

        tick = 0
        T0 = Date.now()
        function compute_view(){


            backend.get_state(function(state) {
                if (state.simulated){
                    tick += 1
                    if (Date.now()-T0 > 100){
                        $('.fps').text("FPS : " + Math.round(1000/((Date.now()-T0)/tick)));
                        T0 = Date.now()
                        tick = 0
                    }
                }

                let present_marker = state.markers
                for (var key in markers) {
                    if(!(key in present_marker)){
                        canvas = markers[key]["context"].canvas
                        markers[key]["context"].clearRect(0,0,canvas.width,canvas.height)
                        markers[key]["clear"] = true
                    }
                }
                for (var entry in present_marker) {

                    robot = present_marker[entry]
                    robot_pos = cam_to_sim(robot.position,robot.orientation)

                    if (if_move(markers[entry]["pos"], robot_pos) || markers[entry]["clear"] || markers[entry]["pos"] != state["leds"][entry]) {
                        markers[entry]["context"].clearRect(-8*ctx_width,-8*ctx_height,8*2*ctx_width,8*2*ctx_height)
                        robot_size = constants["robot_radius"] * 2 * meters_to_pixels_ratio()

                        markers[entry]["context"].rotate(-markers[entry]["pos"][2])
                        markers[entry]["context"].translate(-markers[entry]["pos"][0],-markers[entry]["pos"][1])

                        markers[entry]["context"].translate(robot_pos[0],robot_pos[1])
                        markers[entry]["context"].rotate(robot_pos[2])

                            if (Object.keys(state["leds"]).length != 0){
                                markers[entry]["leds"] = state["leds"][entry]
                                for (var i = 0; i < 3; i++) {
                                    markers[entry]["leds"][i] = Math.round(Math.min(255, 50+Math.log(markers[entry]["leds"][i]+1)/Math.log(256) * 255))
                                }
                                draw_leds(markers[entry]["leds"], markers[entry]["context"])
                            }

                        markers[entry]["context"].drawImage(markers[entry]["image"],-robot_size/2,-robot_size/2,robot_size,robot_size)                 
                        markers[entry]["pos"] = robot_pos
                        markers[entry]["clear"] = false

                    }
                }
                backend.get_wait_ball_position(function(wait_ball_position){
                    if (state.ball != null){
                        draw_ball(state.ball)
                    }
                    if (wait_ball_position != null){
                        draw_circle(cam_to_sim(wait_ball_position), 20, "red", document.getElementById("ball"), false, 1)
                    }
                })

            });
        };

        function resize(){
            simulated_view = !simulated_view
            run_view()
        }
        function resize_canvas(canvas){
                back_canvas = document.getElementById('back')
                canvas.width = back_canvas.offsetWidth
                canvas.height = back_canvas.offsetHeight
                return canvas
        }
        function run_view() {
            if (!simulated_view) {
                $('#ViewChange').html("<i class='bi bi-camera'></i> Camera View")
                $('#vision').addClass('d-none')
                $('#back').removeClass('d-none')
                $('.sim_vim').css('opacity', '100')

                markers = {"blue1":NaN,"blue2":NaN,"green1":NaN,"green2":NaN}
                for(let marker in markers){
                    markers[marker] = {"image":NaN,"context":NaN,"pos":[0,0,0],"leds":[0,0,0],"clear":true}
                }

                for (var key in markers) {
                    markers[key]["image"] = new Image();
                    markers[key]["image"].src = "static/imgs/robot"+ key +".svg"
                    canvas = resize_canvas(document.getElementById(key))
                    markers[key]["context"] = canvas.getContext('2d')
                }
                resize_canvas(document.getElementById("ball"))

                clearInterval(intervalId)
                intervalId = setInterval(compute_view, 1000/30)
                simulated_view = true

            }else{
                clearInterval(intervalId)
                $('#ViewChange').html("<i class='bi bi-camera'></i> Simulated View")
                $('#vision').removeClass('d-none')
                $('#back').addClass('d-none')
                $('.sim_vim').css('opacity', '0')
                simulated_view = false; 

            }
        }

        setTimeout(run_view, 1000)
        window.onresize = resize

        $('#ViewChange').click(run_view)

        backend.is_simulated(function (simulated) {
            if(simulated) {
                $('body').addClass('vision-running')
                let canvas = document.getElementById("ball")
                const distance = (x1, y1, x2, y2) => Math.hypot(x2 - x1, y2 - y1); 
                let drag_type = null
                let initial_position = null
 
                function teleport_selected_object_on_mouse(e){
                    let pos_reel = [0.0, 0.0, 0.0]
                    pos = [...initial_position]

                    if (drag_type == "position") {
                        pos[0] = e.layerX
                        pos[1] = e.layerY
                    } else {
                        pos[2] = Math.atan2(e.layerY - initial_position[1], e.layerX - initial_position[0]) + Math.PI/2
                    }

                    back_canvas = document.getElementById('back')
                    ratio = 1/meters_to_pixels_ratio()
                    pos_reel[0] = (pos[0] - back_canvas.offsetWidth/2) * ratio
                    pos_reel[1] = -(pos[1] - back_canvas.offsetHeight/2) * ratio
                    pos_reel[2] = -(pos[2]-Math.PI/2)
                    backend.teleport(selected_objet, pos_reel[0], pos_reel[1], pos_reel[2])
                }

                canvas.addEventListener("mousedown", function(e) {
                    for (let marker in markers){
                        if (distance(markers[marker]["pos"][0], markers[marker]["pos"][1], e.layerX, e.layerY) < constants["robot_radius"]*meters_to_pixels_ratio()){
                            selected_objet = marker
                        }
                    }
                    drag_type = (e.button == 0) ? "position" : "orientation"
                    if (selected_objet != "ball") {
                        initial_position = markers[selected_objet]["pos"]
                    } else {
                        initial_position = [0., 0., 0.]
                    }

                    canvas.addEventListener("mousemove", teleport_selected_object_on_mouse)
                })
                canvas.addEventListener("mouseup", function(e){ 
                    teleport_selected_object_on_mouse(e)
                    canvas.removeEventListener("mousemove",teleport_selected_object_on_mouse)
                    selected_objet = "ball"
                })
            }
        })
    })
}