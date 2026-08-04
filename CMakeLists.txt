cmake_minimum_required(VERSION 3.20)

project(
    shopify_alibaba_terminal_orchestrator
    VERSION 2.5.0
    DESCRIPTION "Low-resource terminal orchestrator for Shopify and Alibaba"
    LANGUAGES CXX
)

option(COMMERCE_BUILD_TESTS "Build native terminal tests" ON)

add_library(
    commerce_terminal_core
    native/src/action_policy.cpp
    native/src/commands/catalog_commands.cpp
    native/src/commands/command_parser.cpp
    native/src/commands/command_registry.cpp
    native/src/commands/compliance_commands.cpp
    native/src/commands/finance_commands.cpp
    native/src/commands/fulfillment_commands.cpp
    native/src/commands/marketing_commands.cpp
    native/src/commands/order_commands.cpp
    native/src/commands/procurement_commands.cpp
    native/src/commands/system_commands.cpp
    native/src/durable_plan_store.cpp
    native/src/runtime/command_dispatcher.cpp
    native/src/runtime/message_codec.cpp
    native/src/runtime/named_pipe_client.cpp
    native/src/runtime/resource_monitor.cpp
    native/src/runtime/runtime_bridge.cpp
    native/src/runtime/shutdown_controller.cpp
    native/src/runtime/single_output_owner.cpp
    native/src/sha256.cpp
    native/src/terminal/alert_widget.cpp
    native/src/terminal/alternate_screen.cpp
    native/src/terminal/ansi_console_backend.cpp
    native/src/terminal/ascii_sanitizer.cpp
    native/src/terminal/console_backend.cpp
    native/src/terminal/cursor_guard.cpp
    native/src/terminal/diff_renderer.cpp
    native/src/terminal/event_ring.cpp
    native/src/terminal/fixed_line_registry.cpp
    native/src/terminal/input_editor.cpp
    native/src/terminal/keyboard_reader.cpp
    native/src/terminal/metric_widget.cpp
    native/src/terminal/page_registry.cpp
    native/src/terminal/progress_bar.cpp
    native/src/terminal/screen_buffer.cpp
    native/src/terminal/screen_layout.cpp
    native/src/terminal/sparkline.cpp
    native/src/terminal/status_widget.cpp
    native/src/terminal/table_widget.cpp
    native/src/terminal/terminal_size.cpp
    native/src/terminal/win32_console_backend.cpp
    native/src/terminal/widget.cpp
    native/src/terminal_dashboard.cpp
)
target_include_directories(commerce_terminal_core PUBLIC native/include)
target_compile_features(commerce_terminal_core PUBLIC cxx_std_17)
target_compile_definitions(commerce_terminal_core PUBLIC COMMERCE_VERSION="${PROJECT_VERSION}")

if(MSVC)
    target_compile_options(commerce_terminal_core PRIVATE /W4 /permissive- /EHsc)
else()
    target_compile_options(
        commerce_terminal_core
        PRIVATE -Wall -Wextra -Wpedantic -Wconversion -Wshadow
    )
endif()

find_package(Threads REQUIRED)
target_link_libraries(commerce_terminal_core PUBLIC Threads::Threads)

add_executable(shopify_alibaba_terminal native/src/main.cpp)
target_link_libraries(shopify_alibaba_terminal PRIVATE commerce_terminal_core)

if(WIN32)
    target_compile_definitions(shopify_alibaba_terminal PRIVATE WIN32_LEAN_AND_MEAN NOMINMAX)
endif()

include(CTest)
if(BUILD_TESTING AND COMMERCE_BUILD_TESTS)
    add_executable(terminal_core_tests native/tests/test_terminal_core.cpp)
    target_link_libraries(terminal_core_tests PRIVATE commerce_terminal_core)
    add_test(NAME terminal_core_tests COMMAND terminal_core_tests)
    add_executable(terminal_layout_tests native/tests/test_terminal_layout.cpp)
    target_link_libraries(terminal_layout_tests PRIVATE commerce_terminal_core)
    add_test(NAME terminal_layout_tests COMMAND terminal_layout_tests)
    add_executable(native_control_plane_tests native/tests/test_native_control_plane.cpp)
    target_link_libraries(native_control_plane_tests PRIVATE commerce_terminal_core)
    add_test(NAME native_control_plane_tests COMMAND native_control_plane_tests)
    add_test(NAME terminal_self_test COMMAND shopify_alibaba_terminal --self-test)
    add_executable(test_terminal_widgets native/tests/test_terminal_widgets.cpp)
    target_link_libraries(test_terminal_widgets PRIVATE commerce_terminal_core)
    add_test(NAME test_terminal_widgets COMMAND test_terminal_widgets)

    foreach(test_name IN ITEMS
        test_command_parser test_diff_renderer test_event_ring test_fixed_line_registry
        test_input_editor test_message_codec test_resource_monitor test_screen_layout
        test_single_output_owner test_terminal_no_scroll)
        add_executable(${test_name} native/tests/${test_name}.cpp)
        target_link_libraries(${test_name} PRIVATE commerce_terminal_core)
        add_test(NAME ${test_name} COMMAND ${test_name})
    endforeach()
endif()

install(TARGETS shopify_alibaba_terminal RUNTIME DESTINATION bin)
