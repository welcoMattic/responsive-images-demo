<?php

namespace App\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\Routing\Annotation\Route;

class RokkaController extends AbstractController
{
    /**
     * @Route("/rokka", name="rokka")
     */
    public function index()
    {
        return $this->render('rokka/index.html.twig', [
            'controller_name' => 'RokkaController',
        ]);
    }
}
