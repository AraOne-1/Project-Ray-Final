import RT_utility as rtu
import RT_camera as rtc
import RT_renderer as rtren
import RT_material as rtm
import RT_scene as rts
import RT_object as rto
import RT_integrator as rti
import RT_light as rtl
import RT_texture as rtt



USE_FINAL = False

if USE_FINAL:
    IMAGE_WIDTH = 480
    SAMPLES_PER_PIXEL = 16
    MAX_DEPTH = 4
    OUTPUT_NAME = "scene_glass_temple.png"
else:
    IMAGE_WIDTH = 960
    SAMPLES_PER_PIXEL = 64
    MAX_DEPTH = 6
    OUTPUT_NAME = "scene_glass_temple_preview.png"


# ========== CAMERA ==========
def create_camera():
    cam = rtc.Camera()
    cam.aspect_ratio = 16.0 / 9.0
    cam.img_width = IMAGE_WIDTH
    cam.center = rtu.Vec3(0, 0, 0)
    cam.samples_per_pixel = SAMPLES_PER_PIXEL
    cam.max_depth = MAX_DEPTH
    cam.vertical_fov = 32

    cam.look_from = rtu.Vec3(0.5, 1.7, 6.7)
    cam.look_at = rtu.Vec3(0.0, 0.3, -2.2)
    cam.vec_up = rtu.Vec3(0, 1, 0)

    cam.one_over_sqrt_spp = 1.0 / (SAMPLES_PER_PIXEL ** 0.5)

    aperture = 0.06
    focus_distance = 8.0
    cam.init_camera(aperture, focus_distance)

    return cam


# ========== ROOM ==========
def add_room(world):
    wall_gray = rtm.Lambertian(rtu.Color(0.72, 0.72, 0.75))
    left_red = rtm.Lambertian(rtu.Color(0.75, 0.22, 0.22))
    right_green = rtm.Lambertian(rtu.Color(0.22, 0.68, 0.30))

    floor_tex = rtt.CheckerTexture(
        0.60,
        rtu.Color(0.10, 0.10, 0.10),
        rtu.Color(0.82, 0.82, 0.82)
    )
    floor_mat = rtm.TextureColor(floor_tex)

    world.add_object(rto.Quad(
        rtu.Vec3(-6, -1, -9),
        rtu.Vec3(12, 0, 0),
        rtu.Vec3(0, 0, 14),
        floor_mat
    ))

    world.add_object(rto.Quad(
        rtu.Vec3(-6, 5, -9),
        rtu.Vec3(12, 0, 0),
        rtu.Vec3(0, 0, 14),
        wall_gray
    ))

    world.add_object(rto.Quad(
        rtu.Vec3(-6, -1, -9),
        rtu.Vec3(0, 6, 0),
        rtu.Vec3(0, 0, 14),
        left_red
    ))

    world.add_object(rto.Quad(
        rtu.Vec3(6, -1, -9),
        rtu.Vec3(0, 6, 0),
        rtu.Vec3(0, 0, 14),
        right_green
    ))

    world.add_object(rto.Quad(
        rtu.Vec3(-6, -1, -9),
        rtu.Vec3(12, 0, 0),
        rtu.Vec3(0, 6, 0),
        wall_gray
    ))


# ========== OBJECTS ==========
def add_main_objects(world):
    glass = rtm.Dielectric(rtu.Color(0.98, 0.98, 1.00), 1.5)
    gold = rtm.Metal(rtu.Color(0.95, 0.78, 0.30), 0.03)
    blue_metal = rtm.Metal(rtu.Color(0.62, 0.72, 0.95), 0.07)
    dark_matte = rtm.Lambertian(rtu.Color(0.18, 0.18, 0.20))
    glossy_red = rtm.Blinn(rtu.Color(0.78, 0.25, 0.22), 0.70, 0.45, 32)
    glossy_purple = rtm.Blinn(rtu.Color(0.50, 0.35, 0.78), 0.65, 0.50, 24)

    world.add_object(rto.Sphere(rtu.Vec3(-2.0, -0.15, -3.6), 0.85, glass))
    world.add_object(rto.Sphere(rtu.Vec3(0.0, -0.30, -4.1), 0.70, gold))
    world.add_object(rto.Sphere(rtu.Vec3(1.9, -0.10, -3.0), 0.90, glossy_red))
    world.add_object(rto.Sphere(rtu.Vec3(-0.7, -0.65, -1.7), 0.33, blue_metal))
    world.add_object(rto.Sphere(rtu.Vec3(0.8, -0.62, -1.4), 0.36, glossy_purple))
    world.add_object(rto.Sphere(rtu.Vec3(2.8, -0.58, -4.9), 0.42, dark_matte))


# ========== LIGHTS ==========
def add_lights(world):
    warm_light = rtl.Diffuse_light(rtu.Color(5.5, 4.8, 4.2))
    cool_light = rtl.Diffuse_light(rtu.Color(2.2, 2.8, 4.6))
    small_light = rtl.Diffuse_light(rtu.Color(3.4, 2.0, 1.8))

    world.add_object(rto.Sphere(rtu.Vec3(-2.8, 3.1, -2.4), 0.50, warm_light))
    world.add_object(rto.Sphere(rtu.Vec3(2.6, 2.8, -4.2), 0.42, cool_light))
    world.add_object(rto.Sphere(rtu.Vec3(0.0, 4.0, -6.0), 0.28, small_light))


# ========== SCENE ==========
def build_scene():
    world = rts.Scene(rtu.Color(0.0, 0.0, 0.0))
    add_room(world)
    add_main_objects(world)
    add_lights(world)
    return world


# ========== RENDER ==========
def main():
    camera = create_camera()
    world = build_scene()
    integrator = rti.Integrator(bDlight=True, bSkyBG=False)

    renderer = rtren.Renderer(camera, integrator, world)
    renderer.render()
    renderer.write_img2png(OUTPUT_NAME)

    print("Saved:", OUTPUT_NAME)


if __name__ == "__main__":
    main()