import json
import os.path

import cv2
import csv
import time
import numpy as np
import sys
import math
import argparse


# This function is to change frame count to time in millisecond
def frame_count_to_time(frame_count_input, frame_rate_input):
    return (frame_count_input / frame_rate_input) * 1000


# This function is to change time in millisecond to frame count
def time_to_frame_count(time_to_calculate, frame_rate_input):
    return int((time_to_calculate / 1000) * frame_rate_input)


# This function is to read string to convert boolean value
def str_to_bool(input_bool_string):
    if str(input_bool_string).lower().strip() == "true":
        return True
    else:
        return False


# This function is to display the process progressing
def print_percent_done(index_input, total, bar_len=50, title_input='Please wait'):
    percent_done = (index_input + 1) / total * 100
    percent_done_round = round(percent_done, 1)

    done = int(round(percent_done_round / (100 / bar_len)))
    togo = bar_len - done

    done_str = '=' * done
    togo_str = '_' * togo

    sys.stdout.write(f'\r{title_input}: [{done_str}{togo_str}] {percent_done_round}% done')
    sys.stdout.flush()


# This function is to change color string to color tuple value
def change_string_to_color_tuple(input_string):
    if "(" in input_string and ")" in input_string:
        color_value_array = input_string.replace("(", "").replace(")", "").split(",")
        output_color_tuple = tuple(float(index) for index in color_value_array)
        return output_color_tuple
    elif input_string.lower() == "red":
        output_color_tuple = (0, 0, 250)
        return output_color_tuple
    elif input_string.lower() == "green":
        output_color_tuple = (0, 250, 0)
        return output_color_tuple
    elif input_string.lower() == "blue":
        output_color_tuple = (250, 0, 0)
        return output_color_tuple
    elif input_string.lower() == "yellow":
        output_color_tuple = (0, 250, 250)
        return output_color_tuple
    elif input_string.lower() == "black":
        output_color_tuple = (0, 0, 0)
        return output_color_tuple
    elif input_string.lower() == "white":
        output_color_tuple = (250, 250, 250)
        return output_color_tuple
    elif input_string.lower() == "magenta":
        output_color_tuple = (250, 0, 250)
        return output_color_tuple
    elif "#" in input_string.lower():
        value = input_string.lstrip('#')
        lv = len(value)
        if lv == 6:
            try:
                tem_arr = tuple(int(value[xx:xx + lv // 3], 16) for xx in range(0, lv, lv // 3))
                return tem_arr[::-1]
            except ValueError as e:
                print(e)
                raise
        else:
            print(f"The length of input hex string must be 6 character. But it is {lv}.")
            raise
    else:
        print(f"Input string {input_string} is not a valid color string input.")
        print("It can be red, green, blue, black, white or magenta.")
        print("It also can be hex color code.")
        pass


# This function is to get the positions in parent axes array
def get_position_of_parent(search_string_input, axes_array_input):
    idx_found = False
    return_idx = None
    for idx, val in enumerate(axes_array_input):
        if val["name"] == search_string_input:
            idx_found = True
            return_idx = idx
            break

    if not idx_found:
        print(f"{search_string_input} can not be found!")

    return return_idx


# This function is to get the positions in given array
def get_position(search_input, array_in):
    idx_found = False
    return_idx = None
    for idx, val in enumerate(array_in):
        if val == search_input:
            idx_found = True
            return_idx = idx
            break

    if not idx_found:
        print(f"{search_input} can not be found!")

    return return_idx


# This function is to get index value from horizontal to vertical labelling
def get_vertical_position(frame_width_input, frame_height_input, put_text_input,
                          x_input, y_input, color_search_input, font_input, thick_input):
    # width = height and height = width when we rotate the image
    f_w = frame_height_input
    f_h = frame_width_input
    tem_image = np.zeros([int(f_w), int(f_h), 3], dtype=np.uint8)
    x_edit = int(frame_height_input - y_input)
    y_edit = x_input
    co_ord_input = (x_edit, y_edit)
    # draw
    cv2.putText(tem_image, put_text_input, co_ord_input, cv2.FONT_HERSHEY_SIMPLEX, font_input,
                color_search_input, thick_input)
    # rotate
    out_image = cv2.rotate(tem_image, cv2.ROTATE_90_COUNTERCLOCKWISE)
    # capture position to return
    color_index_output = np.where(np.all(out_image == color_search_input, axis=-1))

    return color_index_output


# This function is to get the color index in given image
def get_color_position(image_input, color_in):
    color_index_output = np.where(np.all(image_input == color_in, axis=-1))

    return color_index_output


# This function is to create the data array in order to draw lines in graph
def get_data_array(csv_data_input, t_data_input, y_data_input, offset_input,
                   filter_input=False, filter_by_input=None):
    if filter_input:
        if "=" in filter_by_input:
            filter_name, filter_value, filter_value_type = get_filter_value(filter_by_input)
            data_array_output = []

            with open(csv_data_input, "r") as csv_file:
                csv_reader = (csv.reader(csv_file, delimiter=','))
                header_array = next(csv_reader)
                t_pos = get_position(t_data_input, header_array)
                y_pos = get_position(y_data_input, header_array)
                f_pos = get_position(filter_name, header_array)
                if filter_value_type == "float":
                    for row in csv_reader:
                        filter_check = float(row[f_pos])
                        if filter_check == filter_value:
                            time_value = (float(row[t_pos]) + offset_input) * 1000
                            y_value = float(row[y_pos])
                            data_array_output.append([time_value, y_value])
                elif filter_value_type == "int":
                    for row in csv_reader:
                        filter_check = int(row[f_pos])
                        if filter_check == filter_value:
                            time_value = (float(row[t_pos]) + offset_input) * 1000
                            y_value = float(row[y_pos])
                            data_array_output.append([time_value, y_value])
                else:
                    for row in csv_reader:
                        filter_check = str(row[f_pos])
                        if filter_check == filter_value:
                            time_value = (float(row[t_pos]) + offset_input) * 1000
                            y_value = float(row[y_pos])
                            data_array_output.append([time_value, y_value])

            return data_array_output

        elif "event" in filter_by_input:
            data_array_output = []
            experience_data = False
            first_value_record = False

            with open(csv_data_input, "r") as csv_file:
                csv_reader = (csv.reader(csv_file, delimiter=','))
                header_array = next(csv_reader)
                t_pos = get_position(t_data_input, header_array)
                y_pos = get_position(y_data_input, header_array)
                f_pos = get_position(filter_by_input, header_array)

                for row in csv_reader:
                    event_string_value = str(row[f_pos])
                    if event_string_value != " ":
                        experience_data = True
                        if not first_value_record:
                            first_time_value = (float(row[t_pos]) * 1000)
                            first_value_record = True
                        if event_string_value == "server_end_of_file_message":
                            experience_data = False
                    if experience_data and first_value_record:
                        original_time_value = (float(row[t_pos]) * 1000)
                        time_value = ((float(row[t_pos]) + offset_input) * 1000) - first_time_value
                        y_value = float(row[y_pos])
                        data_array_output.append([time_value, y_value, original_time_value])
            # print(len(data_array_output))
            return data_array_output

    else:
        data_array_output = []
        with open(csv_data_input, "r") as csv_file:
            csv_reader = (csv.reader(csv_file, delimiter=','))
            header_array = next(csv_reader)
            t_pos = get_position(t_data_input, header_array)
            y_pos = get_position(y_data_input, header_array)

            for row in csv_reader:
                time_value = (float(row[t_pos]) + offset_input) * 1000
                y_value = float(row[y_pos])
                data_array_output.append([time_value, y_value])

        return data_array_output


# This function is to get filter by value
def get_filter_value(string_input):
    filter_name, filter_value = str(string_input).split("=")
    if "." in filter_value:
        try:
            filter_value = float(filter_value)
            filter_value_type = "float"
        except ValueError:
            filter_value = str(filter_value)
            filter_value_type = "str"
    else:
        try:
            filter_value = int(filter_value)
            filter_value_type = "int"
        except ValueError:
            filter_value = str(filter_value)
            filter_value_type = "str"

    return filter_name, filter_value, filter_value_type


# This function is to change the given number to scaled value
def number_to_scale(lower_limit_input, upper_limit_input, box_height_input, number_input):
    total_limit = upper_limit_input - lower_limit_input
    number_in_total = number_input - lower_limit_input
    number_output = int(box_height_input * (number_in_total / total_limit))

    return number_output


# This function is to check whether there must be zero line or not
def need_to_display_zero_line(low_limit, up_limit):
    if low_limit < 0 < up_limit:
        return True
    else:
        return False


# This function is to produce average value from array
def get_value_from_array(data_arr_input, low_li, up_li):
    new_arr = data_arr_input[:]
    length_array = len(new_arr)
    if length_array == 1:
        val = new_arr[0]
        return val

    elif length_array == 0:
        val = [((low_li + up_li) / 2), "nothing"]
        return val

    else:
        total_time = 0
        total_value = 0
        for d in new_arr:
            total_time += d[0]
            total_value += d[1]
        avg_time = total_time / length_array
        avg_value = total_value / length_array
        val = [avg_time, avg_value]
        return val


def overlay_graph(draw_able_input, config_info_input, input_video_file, csv_data_to_be_used, output_video_file):
    if draw_able_input and config_info_input:
        axes_array = config_info_input["axes"]
        series_array = config_info_input["series"]
        display_able = str_to_bool(str(config_info_input["display"]))

        input_video = cv2.VideoCapture(input_video_file)
        frame_width = input_video.get(cv2.CAP_PROP_FRAME_WIDTH)
        print("Frame width:", frame_width)
        frame_height = input_video.get(cv2.CAP_PROP_FRAME_HEIGHT)
        print("Frame height:", frame_height)
        frame_rate = input_video.get(cv2.CAP_PROP_FPS)
        print("Frame rate:", frame_rate)
        frame_count = input_video.get(cv2.CAP_PROP_FRAME_COUNT)
        print("Frame count:", frame_count)

        draw_data_array = []
        pointer_info_dict = {}
        max_video_length = math.ceil(frame_count_to_time(frame_count, frame_rate))

        # for loop over series array and prepare the respected data
        for info in series_array:
            search_string = info["parent_axes"]
            parent_index = get_position_of_parent(search_string, axes_array)
            if parent_index is not None:
                axes_info = axes_array[parent_index]
                axes_pos = axes_info["position"]
                # axes_pos_x = axes_pos["x"]
                # axes_pos_y = axes_pos["y"]
                axes_pos_w = axes_pos["width"]
                # axes_pos_h = axes_pos["height"]
                series_name = info["name"]
                pointer_position_name = series_name + "_pointer_info"
                pointer_info_dict[pointer_position_name] = (0, 0)
                display_type = info["display_type"]
                t_limit = info["t-limit"]
                try:
                    t_offset = info["time_offset"]
                except KeyError:
                    t_offset = 0
                t_w = t_limit["width"]
                t_data = info["t_data"]
                y_data = info["y_data"]
                info_filter = str_to_bool(str(info["filter"]))
                filter_by = None
                if info_filter:
                    filter_by = info["filterBy"]
                if str(display_type).lower() == "pen":
                    # getting data from csv with or without filter
                    if info_filter:
                        data_arr = get_data_array(csv_data_to_be_used, t_data, y_data, t_offset, info_filter, filter_by)
                    else:
                        data_arr = get_data_array(csv_data_to_be_used, t_data, y_data, t_offset)
                    series_data_array = []
                    # calculate the max duration of time can be displayed in one pixel
                    time_interval_for_data = round(1000 / (axes_pos_w / t_w), 4)
                    # calculate how many display for the whole video
                    number_of_time_interval = math.ceil(max_video_length / time_interval_for_data)
                    # lower range starts with 0 and upper range starts with milliseconds
                    # calculated from time interval for data
                    lower_range = 0
                    upper_range = round((lower_range + time_interval_for_data), 2)
                    # calculate the length of 1 display in milliseconds
                    width_check = int(t_w) * 1000
                    box_data_array = []
                    for i in range(1, (number_of_time_interval + 1), 1):
                        raw_data_array = []
                        # input_data = None
                        for data in data_arr:
                            if lower_range <= data[0] < upper_range:
                                raw_data_array.append(data)
                        # get the average of value array because we only can draw 1 data at 1 pixel
                        input_data = get_value_from_array(raw_data_array, lower_range, upper_range)
                        box_data_array.append(input_data)
                        if max_video_length <= width_check:
                            if i == (number_of_time_interval - 1):
                                another_box_array = box_data_array[:]
                                series_data_array.append([int(width_check), another_box_array])
                        else:
                            if upper_range >= width_check:
                                another_box_array = box_data_array[:]
                                series_data_array.append([int(width_check), another_box_array])
                                box_data_array.clear()
                                width_check += (int(t_w) * 1000)
                        lower_range = upper_range
                        upper_range = round((upper_range + time_interval_for_data), 2)
                    draw_data_array.append({"series_name": series_name, "display_type": display_type,
                                            "series_data_array": series_data_array})

                elif str(display_type).lower() == "static":
                    # getting data from csv with or without filter
                    if info_filter:
                        data_arr = get_data_array(csv_data_to_be_used, t_data, y_data, t_offset, info_filter, filter_by)
                    else:
                        data_arr = get_data_array(csv_data_to_be_used, t_data, y_data, t_offset)
                    series_data_array = []
                    # calculate the max duration of time can be displayed in one pixel
                    time_interval_for_data = round(1000 / (axes_pos_w / t_w), 4)
                    # calculate how many display for the whole video
                    number_of_time_interval = math.ceil(max_video_length / time_interval_for_data)
                    # lower range starts with 0 and upper range starts with milliseconds
                    # calculated from time interval for data
                    lower_range = 0
                    upper_range = round((lower_range + time_interval_for_data), 2)
                    # calculate the length of 1 display in milliseconds
                    width_check = int(t_w) * 1000
                    box_data_array = []
                    for i in range(1, (number_of_time_interval + 1), 1):
                        raw_data_array = []
                        # input_data = None
                        for data in data_arr:
                            if lower_range <= data[0] < upper_range:
                                raw_data_array.append(data)
                        # get the average of value array because we only can draw 1 data at 1 pixel
                        input_data = get_value_from_array(raw_data_array, lower_range, upper_range)
                        raw_data_array.clear()
                        box_data_array.append(input_data)
                        if max_video_length <= width_check:
                            if i == (number_of_time_interval - 1):
                                another_box_array = box_data_array[:]
                                series_data_array.append([int(width_check), another_box_array])
                        else:
                            if upper_range >= width_check:
                                another_box_array = box_data_array[:]
                                series_data_array.append([int(width_check), another_box_array])
                                box_data_array.clear()
                                width_check += (int(t_w) * 1000)
                        lower_range = upper_range
                        upper_range = round((upper_range + time_interval_for_data), 2)
                    draw_data_array.append({"series_name": series_name, "display_type": display_type,
                                            "series_data_array": series_data_array})

        ret, frame = input_video.read()
        raw_image = None
        if ret:
            # get the frame and fill with black
            raw_image = frame
            raw_image.fill(0)
        box_color_array = []

        for info in series_array:
            search_string = info["parent_axes"]
            parent_index = get_position_of_parent(search_string, axes_array)
            if parent_index is not None:
                axes_info = axes_array[parent_index]
                box_color = axes_info["box_color"]
                axes_pos = axes_info["position"]
                box_title = axes_info["box_title"]
                title_x_position = axes_info["box_title_x_position"]
                title_y_position = axes_info["box_title_y_position"]
                title_color = axes_info["box_title_color"]
                box_color_array.append({"box_color": box_color, "title_color": title_color})
                box_color = change_string_to_color_tuple(box_color)
                title_color = change_string_to_color_tuple(title_color)
                title_font = float(axes_info["box_title_font_scale"])
                box_thickness = int(axes_info["box_thickness"])
                axes_pos_x = axes_pos["x"]
                axes_pos_y = axes_pos["y"]
                axes_pos_w = axes_pos["width"]
                axes_pos_h = axes_pos["height"]
                t_limit = info["t-limit"]
                t_w = t_limit["width"]
                t_name = info["t_label"]
                t_label_x_position = info["t_label_x_position"]
                t_label_y_position = info["t_label_y_position"]
                y_name = info["y_label"]
                y_label_x_position = info["y_label_x_position"]
                y_label_y_position = info["y_label_y_position"]
                label_thickness = int(info["label_thickness"])
                label_font_scale = float(info["label_font_scale"])
                # draw box and labels according to config
                raw_image = cv2.rectangle(raw_image, (axes_pos_x, axes_pos_y),
                                          ((axes_pos_x + axes_pos_w), (axes_pos_y + axes_pos_h)),
                                          box_color, box_thickness)
                title_x = int(axes_pos_x) + int(title_x_position)
                title_y = int(axes_pos_y) - int(title_y_position)
                cv2.putText(raw_image, box_title, (title_x, title_y), cv2.FONT_HERSHEY_SIMPLEX, title_font,
                            title_color, box_thickness)
                t_label_x = int(axes_pos_x) + int(t_label_x_position)
                t_label_y = int(axes_pos_y) + int(t_label_y_position)
                cv2.putText(raw_image, t_name, (t_label_x, t_label_y), cv2.FONT_HERSHEY_SIMPLEX, label_font_scale,
                            box_color, label_thickness)
                y_label_x_input = axes_pos_x - int(y_label_x_position)
                y_label_y_input = axes_pos_y - int(y_label_y_position)
                # getting the position of vertical label
                ver_color_index_array = get_vertical_position(frame_width, frame_height, y_name,
                                                              y_label_x_input, y_label_y_input,
                                                              box_color, label_font_scale, label_thickness)
                # use that position and draw vertical label in raw image
                for item in zip(ver_color_index_array[0], ver_color_index_array[1]):
                    item_tuple = tuple(item)
                    raw_image[item_tuple[0], item_tuple[1]] = box_color

                x_scale_interval_width = int(axes_pos_w / t_w)
                # start_point_x_scale = axes_pos_x
                # x_scale_level = axes_pos_y + axes_pos_h
                height_of_scale = 5

                # draw x axis / t axis interval points
                for i in range(0, t_w):
                    space_value = i * x_scale_interval_width
                    # end_point_x_scale_level = start_point_x_scale - height_of_scale
                    cv2.line(raw_image, (axes_pos_x + space_value,
                                         axes_pos_h + axes_pos_y),
                             (axes_pos_x + space_value,
                              axes_pos_h + axes_pos_y - height_of_scale),
                             box_color, box_thickness)
                # after this points, the raw black image is filled with
                # all graphs and labels

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        v_writer = cv2.VideoWriter(output_video_file, fourcc, int(frame_rate), (int(frame_width), int(frame_height)))
        whole_t = time.time()
        count = 0
        drawing_graph = True

        while drawing_graph:

            # start_tt = time.time()
            ret, frame = input_video.read()
            # end_tt = time.time()
            print_percent_done(count, frame_count)
            check_timer = frame_count_to_time(count, frame_rate)

            if ret:
                for info in series_array:
                    search_string = info["parent_axes"]
                    parent_index = get_position_of_parent(search_string, axes_array)
                    if parent_index is not None:
                        axes_info = axes_array[parent_index]
                        axes_pos = axes_info["position"]
                        x = axes_pos["x"]
                        y = axes_pos["y"]
                        w = axes_pos["width"]
                        h = axes_pos["height"]
                        axes_bg = axes_info["background"]
                        bg_fill = axes_bg["fill"]
                        color_input = change_string_to_color_tuple(bg_fill)
                        bg_opacity = axes_bg["opacity"]
                        # copy a frame to draw boundary
                        overlay_frame = frame.copy()
                        boundary_space = 50
                        # draw boundary to graph
                        cv2.rectangle(overlay_frame,
                                      (x - boundary_space, y - boundary_space),
                                      (x + w + boundary_space,
                                       y + h + boundary_space),
                                      color_input, -1)
                        # overlay by original frame
                        frame = cv2.addWeighted(overlay_frame, bg_opacity,
                                                frame, 1 - bg_opacity, 0)
                        # draw graphs and labels over the frame
                        # to avoid color opacity drops
                        for color in box_color_array:
                            box_color = change_string_to_color_tuple(color["box_color"])
                            title_color = change_string_to_color_tuple(color["title_color"])
                            box_draw_index = get_color_position(raw_image, box_color)
                            title_draw_index = get_color_position(raw_image, title_color)

                            for box_item in zip(box_draw_index[0], box_draw_index[1]):
                                box_item_tuple = tuple(box_item)
                                frame[box_item_tuple[0], box_item_tuple[1]] = box_color

                            for title_item in zip(title_draw_index[0], title_draw_index[1]):
                                title_item_tuple = tuple(title_item)
                                frame[title_item_tuple[0], title_item_tuple[1]] = title_color

                clone_frame = np.copy(frame)

                # for loop and draw the data on the clone frame
                for info in series_array:
                    if len(draw_data_array) > 0:
                        info_name = info["name"]
                        display_arr = None
                        for dic in draw_data_array:
                            if dic["series_name"] == info_name:
                                display_arr = dic["series_data_array"]
                                break
                        search_str = info["parent_axes"]
                        pointer_info = info["pointer_value"]
                        need_to_draw_pointer = bool(pointer_info["Enabled"])
                        line_color = change_string_to_color_tuple(info["line_color"])
                        line_thickness = int(info["line_thickness"])
                        zero_display = str_to_bool(str(info["zero_line_display"]))
                        zero_line_thick = 0
                        if zero_display:
                            zero_line_thick = int(info["zero_line_thickness"])
                        show_type = str(info["display_type"])
                        info_y_limit = info["y-limit"]
                        info_limits = info_y_limit["limits"]
                        lower_limit = info_limits["lower"]
                        upper_limit = info_limits["upper"]
                        can_zero_line_be_drawn = need_to_display_zero_line(lower_limit, upper_limit)
                        info_t_limit = info["t-limit"]
                        t_width = info_t_limit["width"]
                        pointer_color = None
                        pointer_radius = None
                        if need_to_draw_pointer:
                            pointer_color = change_string_to_color_tuple(pointer_info["Color"])
                            pointer_radius = pointer_info["Radius"]
                        parent_index = get_position_of_parent(search_str, axes_array)
                        axes_info = axes_array[parent_index]
                        if show_type == "pen" and parent_index is not None:
                            ax_pos = axes_info["position"]
                            ax_x = ax_pos["x"]
                            ax_y = ax_pos["y"]
                            ax_w = ax_pos["width"]
                            ax_h = ax_pos["height"]
                            if can_zero_line_be_drawn:
                                zero_line_start_x = ax_x
                                zero_line_y_scale = int(number_to_scale(lower_limit, upper_limit, ax_h, 0))
                                zero_line_y = int(ax_y + ax_h - zero_line_y_scale)
                                zero_line_end_x = ax_x + ax_w
                            else:
                                zero_line_start_x = 0
                                zero_line_y_scale = 0
                                zero_line_y = 0
                                zero_line_end_x = 0
                            time_in_pixel_value = round((t_width / ax_w), 20)
                            # print(time_in_pixel_value)
                            time_interval_for_data = round(1 / (ax_w / t_width), 20)
                            start_x = ax_x
                            start_y = 0
                            value_to_draw = False
                            display_count = int(check_timer / (t_width * 1000))
                            total_display_count = int(max_video_length / (t_width * 1000))
                            end_x = 0
                            end_y = 0
                            final_display_arr = display_arr[display_count][1]
                            # pointer_x = 0
                            # pointer_y = 0
                            check_timer_input = check_timer - (display_count * t_width * 1000)
                            drawable_limit = ax_x + int((check_timer_input / (time_interval_for_data * 1000)))
                            pen_draw = False
                            no_first_value = False
                            pointer_position_info_name = info_name + "_pointer_info"

                            if len(final_display_arr) > 0:
                                for ind, num in enumerate(final_display_arr):
                                    if zero_display:
                                        cv2.line(clone_frame, (zero_line_start_x, zero_line_y),
                                                 (zero_line_end_x, zero_line_y),
                                                 line_color, zero_line_thick)
                                    if type(num[1]) == str:
                                        if ind == 0:
                                            no_first_value = True

                                    elif math.isnan(num[1]):
                                        value_to_draw = False

                                    else:
                                        if not value_to_draw:
                                            if no_first_value:
                                                scaled_num = number_to_scale(lower_limit, upper_limit, ax_h, num[1])
                                                start_x = ax_x
                                                start_y = int(ax_y + ax_h - scaled_num)
                                                value_to_draw = True
                                                no_first_value = False
                                            else:
                                                scaled_num = number_to_scale(lower_limit, upper_limit, ax_h, num[1])
                                                # scaled_step = int(round(((num[0] / 1000) / time_in_pixel_value), 0))
                                                scaled_step = math.ceil((num[0] / 1000) / time_in_pixel_value)
                                                start_x = ax_x + scaled_step - (display_count * ax_w)
                                                start_y = int(ax_y + ax_h - scaled_num)
                                                value_to_draw = True
                                        else:
                                            if start_x >= drawable_limit:
                                                pen_draw = False
                                            else:
                                                pen_draw = True
                                            if pen_draw:
                                                scaled_num = number_to_scale(lower_limit, upper_limit, ax_h, num[1])
                                                # scaled_step = int(round(((num[0] / 1000) / time_in_pixel_value), 0))
                                                scaled_step = math.ceil((num[0] / 1000) / time_in_pixel_value)
                                                end_x = ax_x + scaled_step - (display_count * ax_w)
                                                end_y = int(ax_y + ax_h - scaled_num)
                                                cv2.line(clone_frame, (start_x, start_y), (end_x, end_y),
                                                         line_color, line_thickness, cv2.LINE_AA)
                                                if need_to_draw_pointer and round(num[0] / 100, 0) >= round(
                                                        check_timer / 100, 0):
                                                    pointer_info_dict[pointer_position_info_name] = (end_x, end_y)

                                                start_x = end_x
                                                start_y = end_y

                                pointer_position_tuple = pointer_info_dict[pointer_position_info_name]
                                pointer_x = pointer_position_tuple[0]
                                pointer_y = pointer_position_tuple[1]
                                if pointer_x == ax_x or pointer_x == (ax_x + ax_w) or \
                                        pointer_y == ax_y or pointer_y == (ax_y - ax_h):
                                    pass
                                else:
                                    cv2.circle(clone_frame, (pointer_x, pointer_y), pointer_radius, pointer_color, -1)

                        elif show_type == "static" and parent_index is not None:
                            ax_pos = axes_info["position"]
                            ax_x = ax_pos["x"]
                            ax_y = ax_pos["y"]
                            ax_w = ax_pos["width"]
                            ax_h = ax_pos["height"]
                            if can_zero_line_be_drawn:
                                zero_line_start_x = ax_x
                                zero_line_y_scale = int(number_to_scale(lower_limit, upper_limit, ax_h, 0))
                                zero_line_y = int(ax_y + ax_h - zero_line_y_scale)
                                zero_line_end_x = ax_x + ax_w
                            else:
                                zero_line_start_x = 0
                                zero_line_y_scale = 0
                                zero_line_y = 0
                                zero_line_end_x = 0
                            time_in_pixel_value = round((t_width / ax_w), 4)
                            time_interval_for_data = round(1 / (ax_w / t_width), 4)
                            start_x = ax_x
                            start_y = 0
                            value_to_draw = False
                            display_count = int(check_timer / (t_width * 1000))
                            total_display_count = int(max_video_length / (t_width * 1000))
                            end_x = 0
                            end_y = 0
                            final_display_arr = display_arr[display_count][1]
                            pointer_position_info_name = info_name + "_pointer_info"

                            if len(final_display_arr) > 0:
                                for ind, num in enumerate(final_display_arr):
                                    if zero_display:
                                        cv2.line(clone_frame, (zero_line_start_x, zero_line_y),
                                                 (zero_line_end_x, zero_line_y),
                                                 line_color, zero_line_thick)
                                    if type(num[1]) == str:
                                        pass

                                    elif math.isnan(num[1]):
                                        value_to_draw = False

                                    else:
                                        if not value_to_draw:
                                            scaled_num = number_to_scale(lower_limit, upper_limit, ax_h, num[1])
                                            scaled_step = int(round(((num[0] / 1000) / time_in_pixel_value), 0))
                                            start_x = ax_x + scaled_step - (display_count * ax_w)
                                            start_y = int(ax_y + ax_h - scaled_num)
                                            value_to_draw = True
                                        else:
                                            scaled_num = number_to_scale(lower_limit, upper_limit, ax_h, num[1])
                                            scaled_step = int(round(((num[0] / 1000) / time_in_pixel_value), 0))
                                            if display_count != total_display_count and ind == (
                                                    len(final_display_arr) - 1):
                                                end_x = ax_x + ax_w
                                            else:
                                                end_x = ax_x + scaled_step - (display_count * ax_w)
                                            end_y = int(ax_y + ax_h - scaled_num)
                                            cv2.line(clone_frame, (start_x, start_y), (end_x, end_y),
                                                     line_color, line_thickness, cv2.LINE_AA)
                                            if need_to_draw_pointer and (round(num[0] / 5, 0)) * 5 == round(check_timer,
                                                                                                            0):
                                                pointer_info_dict[pointer_position_info_name] = (end_x, end_y)

                                            start_x = end_x
                                            start_y = end_y
                                pointer_position_tuple = pointer_info_dict[pointer_position_info_name]
                                pointer_x = pointer_position_tuple[0]
                                pointer_y = pointer_position_tuple[1]
                                if pointer_x == ax_x or pointer_x == (ax_x + ax_w) or \
                                        pointer_y == ax_y or pointer_y == (ax_y - ax_h):
                                    pass
                                else:
                                    cv2.circle(clone_frame, (pointer_x, pointer_y), pointer_radius, pointer_color, -1)

                    else:
                        print("\r")
                        print("Drawable graph data is not found.")
                        drawing_graph = False

                for info in series_array:
                    search_string = info["parent_axes"]
                    parent_index = get_position_of_parent(search_string, axes_array)
                    if parent_index is not None:
                        axes_info = axes_array[parent_index]
                        axes_pos = axes_info["position"]
                        x = axes_pos["x"]
                        y = axes_pos["y"]
                        w = axes_pos["width"]
                        h = axes_pos["height"]
                        # crop the clone frame to get the graph box
                        cropped_image = clone_frame[y:(y + h), x:(x + w)]
                        # replace on the original frame in order to avoid over drawn
                        frame[y:(y + h), x:(x + w)] = cropped_image

                if display_able:
                    cv2.imshow("Frame", frame)
                    # cv2.imshow("F", clone_frame)
                # vsr_t = time.time()
                v_writer.write(frame)
                # vso_t = time.time()
                count += 1
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                end_whole_t = time.time()
                print("\r")
                print(f"The whole process took {round((end_whole_t - whole_t), 4)} seconds.")
                print(f"{output_video_file} is successfully produced.")
                print("Thank you for using VINSET")
                break

        input_video.release()
        v_writer.release()
        cv2.destroyAllWindows()


def overlay_text(draw_able_input, config_info_input, input_video_file, output_video_file):
    text_info = config_info_input["text_info"]
    text_font_size = text_info["text_font_size"]
    text_color = text_info["text_color"]
    text_color_tuple = change_string_to_color_tuple(text_color)
    text_thickness = text_info["text_thickness"]
    timeline_file_name = config_info_input["timeline_file_name"]
    timeline_file = str(input_video_file).replace(os.path.basename(input_video_file), timeline_file_name)
    timeline_info = None
    stimulus_text_display_location = config_info_input["stimulus_text_display_location"]
    va_text_display_location = config_info_input["va_text_display_location"]
    sti_x_position = stimulus_text_display_location["x"]
    sti_y_position = stimulus_text_display_location["y"]
    va_x_position = va_text_display_location["x"]
    va_y_position = va_text_display_location["y"]
    minimum_va_decimal = text_info["minimum_va_decimal"]

    try:
        f = open(timeline_file)
        timeline_info = json.load(f)
        print(f"{timeline_file} is loaded successfully by json.")
        # print(timeline_info)
    except ValueError:
        draw_able_input = False
        print(f"{timeline_file} cannot be loaded by json.")

    if draw_able_input and config_info_input:
        display_able = str_to_bool(str(config_info_input["display"]))

        input_video = cv2.VideoCapture(input_video_file)
        frame_width = input_video.get(cv2.CAP_PROP_FRAME_WIDTH)
        print("Frame width:", frame_width)
        frame_height = input_video.get(cv2.CAP_PROP_FRAME_HEIGHT)
        print("Frame height:", frame_height)
        frame_rate = input_video.get(cv2.CAP_PROP_FPS)
        print("Frame rate:", frame_rate)
        frame_count = input_video.get(cv2.CAP_PROP_FRAME_COUNT)
        print("Frame count:", frame_count)

        stimulus_level_array = get_logmar_level_array(timeline_info, text_info)

        final_stimulus_level_array = add_logmar_interval(stimulus_level_array, text_info)

        # for d in final_stimulus_level_array:
        #     print(d)
        # return

        max_video_length = math.ceil(frame_count_to_time(frame_count, frame_rate))
        print(f"Video length:{max_video_length / 1000} sec")

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        v_writer = cv2.VideoWriter(output_video_file, fourcc, int(frame_rate), (int(frame_width), int(frame_height)))
        whole_t = time.time()
        count = 0
        drawing_graph = True
        start_drawing = False
        stimulus_display_text = None
        sweep_order = None
        final_stimulus_level_array_length = len(final_stimulus_level_array)
        stimulus_index = 0

        while drawing_graph:

            # start_tt = time.time()
            ret, frame = input_video.read()
            # end_tt = time.time()
            print_percent_done(count, frame_count)
            check_timer = frame_count_to_time(count, frame_rate)

            if ret:
                if stimulus_index < final_stimulus_level_array_length:
                    stimulus_timestamp_to_check = final_stimulus_level_array[stimulus_index]["timestamp"] * 1000
                    if check_timer >= stimulus_timestamp_to_check:
                        start_drawing = True
                        stimulus_display_text = str(final_stimulus_level_array[stimulus_index]["logmar"])
                        sweep_order = final_stimulus_level_array[stimulus_index]["sweep_order"]
                        stimulus_index += 1

                if start_drawing:
                    nearest_stimulus_text = get_nearest_stimulus(stimulus_display_text)
                    cv2.putText(frame, f"Stimulus Level:{str(nearest_stimulus_text)}", (sti_x_position, sti_y_position),
                                cv2.FONT_HERSHEY_SIMPLEX, text_font_size,
                                text_color_tuple, text_thickness)
                    va_display_text = get_va_from_stimulus(str(stimulus_display_text), sweep_order, minimum_va_decimal)
                    cv2.putText(frame, f"VA       Level:{str(va_display_text)}", (va_x_position, va_y_position),
                                cv2.FONT_HERSHEY_SIMPLEX, text_font_size,
                                text_color_tuple, text_thickness)
                    if sweep_order == "resting":
                        start_drawing = False

                if display_able:
                    cv2.imshow("Frame", frame)
                    # cv2.imshow("F", clone_frame)
                    # vsr_t = time.time()
                    v_writer.write(frame)
                    # vso_t = time.time()
                    count += 1
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
            else:
                end_whole_t = time.time()
                print("\r")
                print(f"The whole process took {round((end_whole_t - whole_t), 4)} seconds.")
                print(f"{output_video_file} is successfully produced.")
                print("Thank you for using VINSET")
                break

        input_video.release()
        v_writer.release()
        cv2.destroyAllWindows()


def get_logmar_level_array(timeline_info_info, text_info_input):
    draw_data = []
    text_indicator = text_info_input["text_marker_location"]
    time_indicator = text_info_input["time_marker_location"]
    first_text_indicator, second_text_indicator, third_text_indicator = str(text_indicator).split("->")
    first_time_indicator, second_time_indicator, third_time_indicator = str(time_indicator).split("->")
    minimum_va_decimal = text_info_input["minimum_va_decimal"]
    for event in timeline_info_info:
        first_attribute = str(list(event.keys())[0])
        if first_attribute == first_text_indicator:
            event_info = event[first_attribute]
            time_value = event_info[second_time_indicator][third_time_indicator]
            text_value = str(round((float(event_info[second_text_indicator][third_text_indicator])), 2))
            text_value = check_and_add_decimal(text_value, minimum_va_decimal)
            data = {"timestamp": time_value, "logmar": text_value}
            draw_data.append(data)
    # for data in draw_data:
    #     print(data)

    return draw_data


def add_logmar_interval(draw_data_array_input, text_info_input):
    va_logmar_interval = text_info_input["va_logmar_interval"]
    draw_data_array_length = len(draw_data_array_input)
    last_index = draw_data_array_length - 1
    minimum_va_decimal = text_info_input["minimum_va_decimal"]

    final_data_array = []
    for index in range(draw_data_array_length):
        if index is not last_index:
            first_value = draw_data_array_input[index]
            second_value = draw_data_array_input[index + 1]
            first_logmar = float(first_value["logmar"])
            second_logmar = float(second_value["logmar"])
            first_timestamp = first_value["timestamp"]
            second_timestamp = second_value["timestamp"]

            logmar_diff = first_logmar - second_logmar
            sweep_order = "descending" if logmar_diff >= 0 else "ascending"
            number_of_intervals = int(round(abs(logmar_diff), 1) / va_logmar_interval)
            first_value["sweep_order"] = sweep_order
            second_value["sweep_order"] = sweep_order

            if logmar_diff == 0:
                first_value["sweep_order"] = "resting"
                second_value["sweep_order"] = "resting"
                final_data_array.append(first_value)
                final_data_array.append(second_value)
            else:
                extra_data = number_of_intervals - 1
                each_time_interval_duration = (second_timestamp - first_timestamp) / number_of_intervals
                final_data_array.append(first_value)
                for ind in range(extra_data):
                    time_value = first_timestamp + ((ind + 1) * each_time_interval_duration)
                    if sweep_order == "descending":
                        text_value = str(round((first_logmar - ((ind + 1) * va_logmar_interval)), 2))
                    else:
                        text_value = str(round(first_logmar + ((ind + 1) * va_logmar_interval), 2))
                    data = {"timestamp": time_value, "logmar": text_value, "sweep_order":sweep_order}
                    final_data_array.append(data)
                final_data_array.append(second_value)
    last_data = final_data_array[-1]
    last_data["sweep_order"] = "resting"
    final_data_array = list({dictionary['timestamp']: dictionary for dictionary in final_data_array}.values())

    return final_data_array


def check_and_add_decimal(string_input, min_decimal_input):
    decimal_count = str(string_input)[::-1].find('.')
    if 0 < decimal_count < min_decimal_input:
        num_of_zero_to_add = min_decimal_input - decimal_count
        string_input = string_input + "0" * num_of_zero_to_add
    return string_input


def get_va_from_stimulus(string_input, sweep_order_input, min_decimal_input):
    if sweep_order_input == "descending" or sweep_order_input == "resting":
        output = str(round((float(string_input) + 0.1), 2))
        output_string = check_and_add_decimal(output, min_decimal_input)
    else:
        output = string_input
        output_string = check_and_add_decimal(output, min_decimal_input)
    return output_string


def get_nearest_stimulus(string_input):
    point_index = str(string_input).find(".") + 2
    if point_index > -1:
        string_input = string_input[:point_index]
        if float(string_input) == 0:
            string_input = "0.0"
    return string_input


def main():
    parser = argparse.ArgumentParser(prog='vinset', description='VINSET package.')
    parser.add_argument('--version', action='version', version='4.0.1'),
    parser.add_argument("-i", dest="input_filename", required=True, type=argparse.FileType('r'), default=sys.stdin,
                        help="input mp4 file", metavar="filename.mp4")
    parser.add_argument("-d", dest="input_data_filename", required=False, type=argparse.FileType('r'),
                        default=sys.stdin,
                        help="input csv data file", metavar="filename.csv")
    parser.add_argument("-o", dest="output_filename", required=True, type=argparse.FileType('w'), default=sys.stdout,
                        help="output mp4 file", metavar="filename.mp4")
    parser.add_argument("-c", dest="config_filename", required=True, type=argparse.FileType('r'), default=sys.stdin,
                        help="config json file", metavar="filename.json")
    parser.add_argument("-t", dest="overlay_type", required=False, default=sys.stdin,
                        help="overlay type", metavar="graph or text")

    # get all input name in string
    args = parser.parse_args()
    input_file = args.input_filename.name
    csv_data = args.input_data_filename.name
    output_file = args.output_filename.name
    config_file = args.config_filename.name
    overlay_type = args.overlay_type
    csv_data_input = False if str(csv_data) == "<stdin>" else True
    overlay_type_input = False if "_io.TextIOWrapper" in str(overlay_type) else True

    # start whether the inputs are in correct types or not
    if str(input_file).endswith(".mp4"):
        print("Input file name:", input_file)
    else:
        print("Input file must be mp4.")
    if csv_data_input:
        if str(csv_data).endswith(".csv"):
            print("Input data file name:", csv_data)
        else:
            print("Input data file must be csv.")
    else:
        print("There is no csv data input")
    if str(csv_data).endswith(".csv"):
        print("Input data file name:", csv_data)
    else:
        print("Input data file must be csv.")
    if str(output_file).endswith(".mp4"):
        print("Output file name:", output_file)
    else:
        print("Output file must be mp4.")
    if str(config_file).endswith(".json"):
        print("Config file name:", config_file)
    else:
        print("Config file must be json.")
    if overlay_type_input:
        if str(overlay_type) == "graph" or str(overlay_type) == "text":
            print("Overlay type:", overlay_type)
        else:
            print("Overlay type must be graph or text.")
    else:
        print("There is no overlay type input")

    config_info = None
    draw_able = True
    try:
        f = open(config_file)
        config_info = json.load(f)
        print(f"{config_file} is loaded successfully by json.")
    except ValueError:
        draw_able = False
        print(f"{config_file} cannot be loaded by json.")

    if not overlay_type_input or str(overlay_type) == "graph":
        if csv_data_input:
            overlay_graph(draw_able, config_info, input_file, csv_data, output_file)
        else:
            print("There is no csv data input -d in commandline.")
            print("Please add -d argument in commandline in order to proceed.")
    elif str(overlay_type) == "text":
        overlay_text(draw_able, config_info, input_file, output_file)
    else:
        print("Invalid overlay type input. It must be graph or text.")
