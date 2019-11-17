<?php

namespace App\Controller;

use App\Service\Glide;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Annotation\Route;

class GlideController extends AbstractController
{
    /**
     * @Route("/glide_demo", name="glide_demo")
     */
    public function demo(): Response
    {
        return $this->render('glide/index.html.twig');
    }

    /**
     * @Route("/glide/{filterName}/{imageName}", name="glide", requirements={"imageName"=".+"})
     */
    public function index(Glide $glide, string $filterName, string $imageName): Response
    {
        $filter = $glide->getFilters()[$filterName] ?? [];

        return $glide->getServer()->getImageResponse($imageName, $filter);
    }
}
