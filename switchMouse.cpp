#include <windows.h>
#include <iostream>

// g++ switchMouse.cpp -o switchMouse.exe -luser32

bool switchMouseMode() {
    // 获取当前状态
    BOOL swapped = GetSystemMetrics(SM_SWAPBUTTON);

    // 切换状态
    return SwapMouseButton(!swapped);
}


enum class MouseButtonMode {
    Left,
    Right
};

// 设置主按钮
void SetMouseButtonMode(MouseButtonMode mode)
{
    SwapMouseButton(mode == MouseButtonMode::Right);
}

// 获取当前主按钮
MouseButtonMode GetMouseButtonMode()
{
    return GetSystemMetrics(SM_SWAPBUTTON)
    ? MouseButtonMode::Right
    : MouseButtonMode::Left;
}

// 切换主按钮
MouseButtonMode ToggleMouseButtonMode()
{
    MouseButtonMode newMode =
        (GetMouseButtonMode() == MouseButtonMode::Left)
        ? MouseButtonMode::Right
        : MouseButtonMode::Left;

    SetMouseButtonMode(newMode);
    return newMode;
}


int main() {

    MouseButtonMode mode = ToggleMouseButtonMode();

    std::cout << "Current mode: "
        << (mode == MouseButtonMode::Left ? "Left" : "Right")
        << std::endl;

    Sleep(1000);

    return 0;
}
